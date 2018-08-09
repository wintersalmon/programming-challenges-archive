import difflib
import json
import os
import tempfile
import time
from typing import List, Dict

from tools.settings import SRC_DIR, RES_DIR, TEMP_DIR


class MyModels(object):
    @classmethod
    def save_json(cls, file_path: str, content: Dict):
        with open(file_path, 'w') as file:
            json.dump(content, file)

    @classmethod
    def load_json(cls, file_path: str) -> Dict:
        with open(file_path, 'r') as file:
            return json.load(file)


class ProblemConf(MyModels):
    def __init__(
            self,
            problem_alias: str,
            judge_alias: str,
            problem_id: str,
            cases: List[Dict] = None):
        self._problem_alias = problem_alias
        self._judge_alias = judge_alias
        self._problem_id = problem_id
        self._cases = cases

    @classmethod
    def get_conf_file_path(cls, problem_alias: str):
        return os.path.join(SRC_DIR, problem_alias, '.conf.json')

    def encode(self):
        return {
            'problem_alias': self.problem_alias,
            'judge_alias': self.judge_alias,
            'problem_id': self.problem_id,
            'cases': self.cases
        }

    def save(self):
        conf_file_path = self.get_conf_file_path(self.problem_alias)
        self.save_json(conf_file_path, self.encode())

    @classmethod
    def load(cls, problem_alias: str):
        conf_file_path = cls.get_conf_file_path(problem_alias)
        conf = cls.load_json(conf_file_path)
        return cls(**conf)

    @property
    def problem_alias(self):
        return self._problem_alias

    @property
    def judge_alias(self):
        return self._judge_alias

    @property
    def problem_id(self):
        return self._problem_id

    @property
    def cases(self):
        return self._cases

    def __repr__(self):
        return 'Problem\n\tname: {problem_alias}\n\tcode: {judge_alias}/{problem_id}\n\tcases: {cases}'.format(
            problem_alias=self.problem_alias,
            judge_alias=self.judge_alias,
            problem_id=self.problem_id,
            cases=[(c['id'], c['options'] if 'options' in c else []) for c in self.cases]
        )


class RunnableProblem(ProblemConf):
    def run_all_cases(self, *, show_details: bool = False, save_results: bool = False):
        for case in self.cases:
            self._run_and_compare(case, show_details=show_details, save_results=save_results)

    def run_one_case(self, case_id: str, *, show_details: bool = False, save_results: bool = False):
        target_case = None
        for case in self.cases:
            if case_id == case['id']:
                target_case = case
                break
        if target_case is None:
            print('case not found: {}'.format(case_id))
        else:
            self._run_and_compare(target_case, show_details=show_details, save_results=save_results)

    def _run_and_compare(self, case, *, show_details: bool = False, save_results: bool = False):
        print('- with case {}: '.format(case['id']), end='')

        if 'options' in case and 'skip' in case['options']:
            print('[       ] SKIP'.format(case['id']))
            return

        case_id = case['id']
        src_file_path = os.path.join(SRC_DIR, self.problem_alias, 'solution.py')
        in_file_path = os.path.join(RES_DIR, self.judge_alias, self.problem_id, case_id, 'in.txt')
        out_file_path = os.path.join(RES_DIR, self.judge_alias, self.problem_id, case_id, 'out.txt')

        if save_results:
            temp_result_file = None
            result_file_path = os.path.join(TEMP_DIR, '.'.join((self.problem_alias, case['id'], 'txt')))
        else:
            temp_result_file = tempfile.NamedTemporaryFile()
            result_file_path = temp_result_file.name

        exe_time = self.run(
            in_file_path=in_file_path,
            out_file_path=result_file_path,
            src_file_path=src_file_path)

        cmp_result = self.compare(
            from_file_path=out_file_path,
            to_file_path=result_file_path)

        if temp_result_file is not None:
            temp_result_file.close()

        running_time_fmt = '{:7.4f}'.format(exe_time)
        compare_result_fmt = 'OK' if not cmp_result else 'FAIL'

        print('[{}] {}'.format(running_time_fmt, compare_result_fmt))

        if show_details:
            for line in cmp_result:
                print(line)

    @classmethod
    def run(cls, in_file_path, out_file_path, src_file_path):
        start = time.time()
        os.system(
            "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
                in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
        return time.time() - start

    @classmethod
    def compare(cls, from_file_path, to_file_path):
        with open(from_file_path, 'r') as from_file, open(to_file_path, 'r') as to_file:
            file_diff = difflib.unified_diff(
                from_file.readlines(),
                to_file.readlines(),
                fromfile='FromFile',
                tofile='ToFile',
                lineterm='')
            return [line for line in file_diff]
