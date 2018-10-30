import getopt
from enum import Enum

from tools.errors import InvalidCommandError
from tools.problems import ProblemFactory


class BaseCommand(object):
    PATH_SEP = '/'
    CASE_SEP = ':'

    HELP_MESSAGE = "EMPTY"

    def __init__(self, *args):
        self._args = args

    def run(self):
        raise NotImplementedError

    @classmethod
    def display_help_message(cls, error_message=None):
        if error_message:
            print(error_message)

        print(cls.HELP_MESSAGE)

    @classmethod
    def retrieve_url(cls, target):
        path = target.split(cls.PATH_SEP)

        if cls.CASE_SEP in path[-1]:
            path[-1], case = path[-1].split(cls.CASE_SEP)
        else:
            case = None

        return path, case


class CommandList(BaseCommand):
    HELP_MESSAGE = "$ python pca.py list [judge_alias]/[problem_alias]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 1:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        path, __ = self.retrieve_url(args[0])
        if len(path) == 2:
            self._judge, self._problem = path
        else:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

    def run(self):
        try:
            problem = ProblemFactory.load(self._judge, self._problem)
            problem.display_status()
            for case_id, case in problem.cases.items():
                print('  {}: {}'.format(case_id, case))

        except FileNotFoundError:
            print('Problem Not Found')


class CommandCreate(BaseCommand):
    HELP_MESSAGE = "$ python pca.py create [judge_alias]/[problem_alias] [judge_id]/[problem_id]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 2:
            self.display_help_message('Invalid Parameters: {}'.format(self._args))
            raise InvalidCommandError

        src_path, __ = self.retrieve_url(args[0])

        if len(src_path) == 2:
            self._judge_alias, self._problem_alias = src_path
        else:
            self.display_help_message('Invalid Parameters: {}'.format(self._args))
            raise InvalidCommandError

        res_path, __ = self.retrieve_url(args[1])

        if len(res_path) == 2:
            self._judge_id, self._problem_id = res_path
        else:
            self.display_help_message('Invalid Parameters: {}'.format(self._args))
            raise InvalidCommandError

    def run(self):
        try:
            ProblemFactory.create(self._judge_alias, self._problem_alias, self._judge_id, self._problem_id)
        except FileExistsError as e:
            print(e)


class CommandExecute(BaseCommand):
    HELP_MESSAGE = "$ python pca.py execute [options] [judge_alias]/[problem_alias]/[case_id]"

    def __init__(self, *args):
        super().__init__(*args)
        try:
            opts, args = getopt.getopt(self._args, "ds", ["detail", "save"])
        except getopt.GetoptError:
            self.display_help_message('Invalid Options: {}'.format(self._args))
            raise InvalidCommandError

        if len(args) != 1:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        src_path, case = self.retrieve_url(args[0])

        if len(src_path) == 2:
            self._judge, self._problem = src_path
            self._case = case
        else:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

        self._detailed_output = False
        self._save_output = False

        for opt, value in opts:
            if opt in ('-s', '--save'):
                self._save_output = True
            elif opt in ('-d', '--detail'):
                self._detailed_output = True

    def run(self):
        try:
            problem = ProblemFactory.load(self._judge, self._problem)

            if self._case:
                problem.run(self._case, save_output=self._save_output, detailed_output=self._detailed_output)
            else:
                problem.run(save_output=self._save_output, detailed_output=self._detailed_output)

        except FileNotFoundError as e:
            print('Problem Not Found', e)


class CommandSkipCase(BaseCommand):
    HELP_MESSAGE = "$ python pca.py skipcase [judge_alias]/[problem_alias]/[case_id]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 1:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        src_path, case = self.retrieve_url(args[0])

        if len(src_path) == 2:
            self._judge, self._problem = src_path
            self._case = case
        else:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

    def run(self):
        try:
            problem = ProblemFactory.load(self._judge, self._problem)

            prev_status = problem.cases[self._case].skip
            problem.cases[self._case].skip = not prev_status
            problem.save()

            problem.display_status()
            for case_id, case in problem.cases.items():
                if case_id == self._case:
                    print(' *{}: {}'.format(case_id, case))
                else:
                    print('  {}: {}'.format(case_id, case))

        except FileNotFoundError:
            print('Problem Not Found')
        except KeyError:
            print('Case Not Found: {}'.format(self._case))


class CommandCreateCase(BaseCommand):

    def run(self):
        print('createcase')


class CommandRemoveCase(BaseCommand):

    def run(self):
        print('removecase')


class CommandCode(Enum):
    HELP = 'help'
    LIST = 'list'
    CREATE = 'create'
    EXECUTE = 'execute'
    SKIP_CASE = 'skipcase'
    CREATE_CASE = 'createcase'
    REMOVE_CASE = 'removecase'


class CommandFactory(object):
    COMMAND_FUNC = {
        CommandCode.LIST: CommandList,
        CommandCode.CREATE: CommandCreate,
        CommandCode.EXECUTE: CommandExecute,
        CommandCode.SKIP_CASE: CommandSkipCase,
        CommandCode.CREATE_CASE: CommandCreateCase,
        CommandCode.REMOVE_CASE: CommandRemoveCase,
    }

    @classmethod
    def display_all_help_message(cls):
        print("""
    $ python pca.py <COMMAND> [OPTIONS] [PARAMS]

    ## General ##
    
    $ python pca.py help
    
    
    ## Problem Related ##
    
    $ python pca.py list <judge_alias>/<problem_alias>
    
    $ python pca.py create [judge_alias]/[problem_alias] [judge_id]/[problem_id]
    
    $ python pca.py [-sd] [--save --detailed] execute <judge_alias>/<problem_alias>/<case_id>
    
    
    ## Case Related ##
    
    $ python pca.py skipcase <judge_alias>/<problem_alias>/<case_id>
    
    $ python pca.py createcase <judge_alias>/<problem_alias>/<case_id>
    
    $ python pca.py removecase <judge_alias>/<problem_alias>/<case_id>""")

    @classmethod
    def execute_from_command_line(cls, args):
        command, params = args[0], args[1:]

        if command == 'help':
            cls.display_all_help_message()
            return

        try:
            command = CommandCode(command)
            command = cls.COMMAND_FUNC[command](*params)
            command.run()

        except ValueError as e:
            raise InvalidCommandError(
                'Unknown command: {}'.format(command)
            ) from e
