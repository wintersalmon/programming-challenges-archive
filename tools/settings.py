import os
import sys

SRC_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SRC_DIR)

# get target category name
# get target problem name
# get target case name if case name was given

# find category directory
# find category/problem directory
# find category/problem/case directory

# print

"""


default
simple
find


"""


def show_usage(error_msg=None):
    if error_msg:
        print(error_msg)
    # print("main.py play <package> [--cli]    # create new game")
    # print("main.py replay <package> [--cli]  # load saved game in replay mode")
    # print("    --cli: load game in CLI(command line interface) mode")


"""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help", "cli"])
    except getopt.GetoptError as e:
        show_usage(str(e))
        sys.exit(1)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            show_usage()
            sys.exit()
        elif opt == "--cli":
            game_ui = GAME_UI_CLI

    try:
        game_mode = args[0]
        if game_mode not in (GAME_COMMAND_RUN, GAME_COMMAND_REPLAY):
            show_usage("invalid command {}".format(game_mode))
            sys.exit(2)
        game_name = args[1]

    except IndexError:
        show_usage("invalid arguments")
        sys.exit(3)

"""


def find_case_path(base_path, category, problem):
    target_path = os.path.join(base_path, category, problem)

    cases = list()
    for root, dirs, files in os.walk(target_path):
        for file in files:
            if file.endswith("in.txt"):
                case_path = root
                cases.append(case_path)
    return sorted(cases)


def main():
    category = sys.argv[1]
    problem = sys.argv[2]

    cases = find_case_path(base_path=ROOT_DIR, category=category, problem=problem)

    if cases:
        for c in cases:
            print(c)
        exit(0)
    else:
        exit(1)


if __name__ == '__main__':
    main()
