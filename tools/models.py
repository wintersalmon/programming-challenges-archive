import os
import time

from typing import List


class MyModels(object):
    def save(self):
        pass

    @classmethod
    def load(cls, *args, **kwargs):
        pass


class Case(MyModels):
    def __init__(self,
                 name: str,
                 user: str,
                 date: str,
                 votes: str,
                 options: List[str]):
        self._name = name
        self._user = user
        self._date = date
        self._votes = votes
        self._options = options


class Problem(MyModels):
    def __init__(self,
                 alias: str,
                 judge: str,
                 problem: str,
                 cases: List[Case] = None):
        self._alias = alias
        self._judge = judge
        self._problem = problem
        self._cases = cases

    @property
    def alias(self):
        return self._alias

    @property
    def judge(self):
        return self._judge

    @property
    def problem(self):
        return self._problem

    @property
    def cases(self):
        return self._cases


class RunnableProblem(Problem):
    def run_all_cases(self):
        pass

    def run_one_case(self, case_alias: str):
        pass

    @classmethod
    def run(cls, in_file_path, out_file_path, src_file_path):
        start = time.time()
        os.system(
            "cat {in_file_path} | python {src_file_path} > {out_file_path}".format(
                in_file_path=in_file_path, out_file_path=out_file_path, src_file_path=src_file_path))
        return time.time() - start
