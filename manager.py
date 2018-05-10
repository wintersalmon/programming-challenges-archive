import sys

from tools.create import create
from tools.run import run_all_script


# def show_usage(error_msg=None):
#     if error_msg:
#         print(error_msg)
#     # print("main.py play <package> [--cli]    # create new game")
#     # print("main.py replay <package> [--cli]  # load saved game in replay mode")
#     # print("    --cli: load game in CLI(command line interface) mode")

def main():
    command = sys.argv[1]
    judge_alias = sys.argv[2]
    problem_id = sys.argv[3]
    case_number = sys.argv[4] if len(sys.argv) == 5 else 'all'

    if command == 'run':
        run_all_script(judge_alias, problem_id)
    elif command == 'new':
        create(judge_alias, problem_id)
    else:
        print('Invalid command', command)
        exit(1)


if __name__ == '__main__':
    main()
    # create('uva', '100')
    # run('uva', '100')
    # run('test', 'echo')
