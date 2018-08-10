from tools.models import ProblemConf


def toggle(problem_alias: str, case_id: str, option_name: str):
    problem = ProblemConf.load(problem_alias)
    try:
        case = problem.cases[case_id]

        if option_name in case['options']:
            case['options'].remove(option_name)
            action = 'removed'

        else:
            case['options'].append(option_name)
            action = 'added'

        problem.save()

        print('case option {action}: {case_id} {option_name}'.format(
            action=action,
            case_id=case_id,
            option_name=option_name))

    except KeyError:
        print('case does not exist: {}'.format(case_id))
