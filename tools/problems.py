import difflib
import json
import os
import tempfile
import time
from enum import Enum

from tools.errors import APIError
from tools.files import create_empty_directory, create_text_file, create_json_file, lazy_create_text_file
from tools.settings import SRC_DIR, RES_DIR, TEMP_DIR, secret_settings
from tools.udebug import UdebugAPI, find_and_get_pdf_content


class IOFileType(Enum):
    TEXT = 'text'
    JSON = 'json'


class BaseProblem(object):
    DEFAULT_IO_FILE_TYPE = IOFileType.TEXT

    def __init__(self, judge, problem, judge_alias, problem_alias, *, cases=None, io_file_type=None):
        self.judge_id = judge
        self.problem_id = problem
        self.judge_alias = judge_alias
        self.problem_alias = problem_alias

        if cases is None:
            self.cases = dict()
        else:
            self.cases = cases

        if io_file_type is None:
            self.io_file_type = self.DEFAULT_IO_FILE_TYPE
        else:
            self.io_file_type = IOFileType(io_file_type)

    def get_res_dir(self):
        return os.path.join(RES_DIR, self.judge_id, self.problem_id)

    def get_src_dir(self):
        return os.path.join(SRC_DIR, self.judge_alias, self.problem_alias)

    def encode(self):
        return {
            "judge": self.judge_id,
            "problem": self.problem_id,
            "cases": self.cases,
            "io_file_type": self.io_file_type.value,
        }

    def save(self):
        with open(self.get_conf_file_path(self.judge_alias, self.problem_alias), 'w') as file:
            json.dump(self.encode(), file, indent=2, separators=(',', ': '))

    def __str__(self):
        return 'Problem: {judge_alias}/{problem_alias} ( {judge_id} / {problem_id} )'.format(
            judge_id=self.judge_id,
            problem_id=self.problem_id,
            judge_alias=self.judge_alias,
            problem_alias=self.problem_alias,
        )

    @classmethod
    def get_conf_file_path(cls, judge_alias, problem_alias):
        return os.path.join(SRC_DIR, judge_alias, problem_alias, '.conf.json')

    @classmethod
    def get_solution_file_path(cls, judge_alias, problem_alias):
        return os.path.join(SRC_DIR, judge_alias, problem_alias, 'solution.py')

    @classmethod
    def get_in_case_file_path(cls, judge_id, problem_id, case_id):
        return os.path.join(RES_DIR, judge_id, problem_id, case_id, 'in.txt')

    @classmethod
    def get_out_case_file_path(cls, judge_id, problem_id, case_id):
        return os.path.join(RES_DIR, judge_id, problem_id, case_id, 'out.txt')


class RunnableProblem(BaseProblem):

    def run(self, case_id, *, save_output=False, detailed_output=False):
        print(self)
        self._run(case_id, save_output=save_output, detailed_output=detailed_output)

    def run_all(self, *, save_output=False, detailed_output=False):
        print(self)
        for case_id in self.cases.keys():
            self._run(case_id, save_output=save_output, detailed_output=detailed_output)

    def _run(self, case_id, *, save_output=False, detailed_output=False):
        raise NotImplementedError


class TextIOProblem(RunnableProblem):

    @classmethod
    def io_file_execute(cls, in_file_path, out_file_path, src_file_path):
        start = time.time()
        os.system(
            "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
                in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
        return time.time() - start

    @classmethod
    def io_file_compare(cls, from_file_path, to_file_path):
        with open(from_file_path, 'r') as from_file, open(to_file_path, 'r') as to_file:
            file_diff = difflib.unified_diff(
                from_file.readlines(),
                to_file.readlines(),
                fromfile='FromFile',
                tofile='ToFile',
                lineterm='')
            return [line for line in file_diff]

    def _run(self, case_id, *, save_output=False, detailed_output=False):
        print('- with case {}: '.format(case_id), end='')

        if 'skip' in self.cases[case_id]['options']:
            print('[       ] SKIP')
            return

        src_file_path = self.get_solution_file_path(self.judge_alias, self.problem_alias)
        in_file_path = self.get_in_case_file_path(self.judge_id, self.problem_id, case_id)
        out_file_path = self.get_out_case_file_path(self.judge_id, self.problem_id, case_id)

        if save_output:
            temp_result_file = None
            result_file_path = os.path.join(TEMP_DIR, '{case_id}.txt'.format(case_id=case_id))
        else:
            temp_result_file = tempfile.NamedTemporaryFile()
            result_file_path = temp_result_file.name

        exe_time = self.io_file_execute(
            in_file_path=in_file_path,
            out_file_path=result_file_path,
            src_file_path=src_file_path)

        cmp_result = self.io_file_compare(
            from_file_path=out_file_path,
            to_file_path=result_file_path)

        if temp_result_file is not None:
            temp_result_file.close()

        print('[{exe_time:7.4f}] {result_msg}'.format(
            exe_time=exe_time,
            result_msg='FAIL' if cmp_result else 'OK'))

        if detailed_output:
            for line in cmp_result:
                print(line)

        return exe_time, cmp_result


class JsonIOProblem(RunnableProblem):

    def _run(self, case_id, *, save_output=False, detailed_output=False):
        import importlib.util
        spec = importlib.util.spec_from_file_location("solution",
                                                      self.get_solution_file_path(self.judge_alias, self.problem_alias))
        solution = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(solution)
        solution()

    @classmethod
    def get_in_case_file_path(cls, judge_id, problem_id, case_id):
        return os.path.join(RES_DIR, judge_id, problem_id, case_id, 'in.json')

    @classmethod
    def get_out_case_file_path(cls, judge_id, problem_id, case_id):
        return os.path.join(RES_DIR, judge_id, problem_id, case_id, 'out.json')


class ProblemFactory(object):

    @classmethod
    def get_src_path(cls, judge, problem, *args):
        base_path = os.path.join(SRC_DIR, judge, problem)

        if args:
            return os.path.join(base_path, *args)
        else:
            return base_path

    @classmethod
    def get_res_path(cls, judge, problem, *args):
        base_path = os.path.join(RES_DIR, judge, problem)

        if args:
            return os.path.join(base_path, *args)
        else:
            return base_path

    @classmethod
    def load(cls, judge_alias, problem_alias):

        with open(cls.get_src_path(judge_alias, problem_alias, '.conf.json'), 'r') as file:
            try:
                content = json.load(file)
                content["judge_alias"] = judge_alias
                content["problem_alias"] = problem_alias

                if "io_file_type" in content and content["io_file_type"] == "json":
                    return JsonIOProblem(**content)
                else:
                    return TextIOProblem(**content)

            except json.decoder.JSONDecodeError as e:
                raise FileNotFoundError('invalid json file') from e

    @classmethod
    def create(cls, judge_id, problem_id, judge_alias, problem_alias):
        try:
            problem = cls.load(judge_alias, problem_alias)

            if problem.judge_id != judge_id or problem.problem_id != problem_id:
                raise FileExistsError('Duplicate Alias Exists: {}/{}'.format(judge_alias, problem_alias))

        except FileNotFoundError:
            problem = BaseProblem(
                judge=judge_id,
                problem=problem_id,
                judge_alias=judge_alias,
                problem_alias=problem_alias,
            )

        api = UdebugAPI(secret_settings['username'], secret_settings['password'])

        if api.is_correct_problem(judge_id, problem_id):
            problem.io_file_type = IOFileType.TEXT
            try:
                input_list = api.get_input_list(judge_id, problem_id)
                loaded_cases = tuple(case['id'] for case in input_list)

            except APIError:
                loaded_cases = tuple()
        else:
            problem.io_file_type = IOFileType.JSON
            loaded_cases = tuple()

        create_json_file(cls.get_src_path(judge_alias, problem_alias, '.conf.json'))
        create_text_file(cls.get_src_path(judge_alias, problem_alias, 'solution.py'))
        create_text_file(cls.get_src_path(judge_alias, problem_alias, 'readme.md'))
        create_empty_directory(cls.get_res_path(judge_id, problem_id))

        if problem.io_file_type == IOFileType.TEXT:
            for case_id in loaded_cases:
                if case_id not in problem.cases:
                    problem.cases[case_id] = {"options": list()}

                in_case_path = cls.get_res_path(judge_id, problem_id, case_id, 'in.txt')
                lazy_create_text_file(in_case_path, lazy_content=lambda: api.get_input(case_id))

                out_case_path = cls.get_res_path(judge_id, problem_id, case_id, 'out.txt')
                lazy_create_text_file(out_case_path, lazy_content=lambda: api.get_output(case_id))

            lazy_create_text_file(
                path=cls.get_res_path(judge_id, problem_id, '{}_{}.pdf'.format(judge_id, problem_id)),
                lazy_content=lambda: find_and_get_pdf_content(judge_id, problem_id),
                is_binary=True
            )

        problem.save()
        return problem
