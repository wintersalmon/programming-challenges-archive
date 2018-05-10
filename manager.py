import sys

from tools.create import create
from tools.run import run_all_script
from tools.update import update


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    print("manager.py run <judge_id> <problem_id> [case_id] # find and run all cases or specific case")
    print("manager.py new <judge_id> <problem_id>  # find judge_problem online and create and download all cases")
    print("manager.py update <judge_id> <problem_id> <case_id> [*options]  # toggle case options")


def main():
    command = sys.argv[1]
    judge_id = sys.argv[2]
    problem_id = sys.argv[3]
    case_id = sys.argv[4] if len(sys.argv) > 4 else 'all'

    if command == 'run':
        run_all_script(judge_id, problem_id)
    elif command == 'new':
        create(judge_id, problem_id)
    elif command == 'update':
        update(judge_id, problem_id, case_id, *sys.argv[5:])
    else:
        show_usage('Invalid command: {}'.format(command))
        exit(1)


if __name__ == '__main__':
    main()
    # create('uva', '100')
    # run('uva', '100')
    # run('test', 'echo')
