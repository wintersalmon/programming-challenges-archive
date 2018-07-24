import getopt
import sys

from tools.create import create
from tools.run import run_all_cases, run_one_case
from tools.update import update


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hsv", ["help", "save", "detail"])
    except getopt.GetoptError as e:
        show_usage(str(e))
        sys.exit(1)

    save_results = False
    show_details = False

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt in ("-s", "--save"):
            save_results = True
        elif opt in ("-v", "--detail"):
            show_details = True

    command = args[0]
    judge_id = args[1]
    problem_id = args[2]

    if command == 'run':
        if len(args) == 3:
            run_all_cases(judge_id, problem_id, save_results=save_results, show_details=show_details)
        elif len(args) == 4:
            case_id = args[3]
            run_one_case(judge_id, problem_id, case_id, save_results=save_results, show_details=show_details)
        else:
            show_usage('Invalid arguments: {}'.format(*args))
            exit(1)

    elif command == 'new':
        create(judge_id, problem_id)

    elif command == 'update':
        if len(args) > 4:
            case_id = args[3]
            options = args[4:]
            update(judge_id, problem_id, case_id, *options)
        else:
            show_usage('Invalid arguments: {}'.format(*args))
            exit(2)

    else:
        show_usage('Invalid command: {}'.format(command))
        exit(3)


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    print("manager.py run <judge_id> <problem_id> [case_id] # find and run all cases or specific case")
    print("manager.py new <judge_id> <problem_id>  # find judge_problem online and create and download all cases")
    print("manager.py update <judge_id> <problem_id> <case_id> [*options]  # toggle case options")
    print()
    print("options:")
    print("-h --help: display help message")
    print("-v --detail: display compare diff details")
    print("-s --save: save results to temp folder")


if __name__ == '__main__':
    main()