import sys

from tools.commands import CommandFactory


def main():
    CommandFactory.execute_from_command_line(sys.argv[1:])


if __name__ == '__main__':
    main()
