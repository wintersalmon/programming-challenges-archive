import difflib
import json
import os
import tempfile
import time
from typing import Dict

from tools.settings import SRC_DIR, RES_DIR, TEMP_DIR


class MyModels(object):
    @classmethod
    def save_json(cls, file_path: str, content: Dict):
        with open(file_path, 'w') as file:
            json.dump(content, file, indent=2, separators=(',', ': '))

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
            cases: Dict[str, Dict] = None):
        self._problem_alias = problem_alias
        self._judge_alias = judge_alias
        self._problem_id = problem_id
        self._cases = cases

    @classmethod
    def get_conf_file_path(cls, problem_alias: str):
        return os.path.join(SRC_DIR, problem_alias, '.conf.json')

    def encode(self):
        return {
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
        conf['problem_alias'] = problem_alias
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
        return 'Problem\n  name: {problem_alias}\n  code: {judge_alias}/{problem_id}\n  cases: {cases}'.format(
            problem_alias=self.problem_alias,
            judge_alias=self.judge_alias,
            problem_id=self.problem_id,
            cases=json.dumps(self.cases, indent=2, separators=('  ', ': '))
        )

    def __eq__(self, other):
        if isinstance(other, ProblemConf):
            return (self.judge_alias, self.problem_id) == (other.judge_alias, other.problem_id)
        raise NotImplementedError

    def __ne__(self, other):
        return not self.__eq__(other)


class RunnableProblem(ProblemConf):
    def run_all_cases(self, *, show_detail: bool = False, save_result: bool = False):
        for case_id in self.cases.keys():
            self.run(case_id, show_detail=show_detail, save_result=save_result)

    def run(self, case_id: str, *, show_detail: bool = False, save_result: bool = False):
        try:
            self.run_and_compare(case_id, show_detail=show_detail, save_result=save_result)
        except KeyError:
            print('case not found: {}'.format(case_id))

    def run_and_compare(self, case_id: str, *, show_detail: bool = False, save_result: bool = False):
        print('- with case {}: '.format(case_id), end='')

        if 'skip' in self.cases[case_id]['options']:
            print('[       ] SKIP')
            return

        src_file_path = os.path.join(SRC_DIR, self.problem_alias, 'solution.py')
        in_file_path = os.path.join(RES_DIR, self.judge_alias, self.problem_id, case_id, 'in.txt')
        out_file_path = os.path.join(RES_DIR, self.judge_alias, self.problem_id, case_id, 'out.txt')

        if save_result:
            temp_result_file = None
            result_file_path = os.path.join(TEMP_DIR, '{case_id}.txt'.format(case_id=case_id))
        else:
            temp_result_file = tempfile.NamedTemporaryFile()
            result_file_path = temp_result_file.name

        exe_time = self.execute(
            in_file_path=in_file_path,
            out_file_path=result_file_path,
            src_file_path=src_file_path)

        cmp_result = self.compare(
            from_file_path=out_file_path,
            to_file_path=result_file_path)

        if temp_result_file is not None:
            temp_result_file.close()

        print('[{exe_time:7.4f}] {result_msg}'.format(
            exe_time=exe_time,
            result_msg='FAIL' if cmp_result else 'OK'))

        if show_detail:
            for line in cmp_result:
                print(line)

        return exe_time, cmp_result

    @classmethod
    def execute(cls, in_file_path, out_file_path, src_file_path):
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
