from tools.models import ProblemConf


def show(problem_alias: str):
    problem = ProblemConf.load(problem_alias)

    print(problem)
