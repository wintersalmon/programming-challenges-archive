import getopt
import re
from enum import Enum

from tools.errors import InvalidCommandError
from tools.problems import ProblemFactory


class BaseCommand(object):
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
    def slash_separated_values(cls, target):
        result = re.match(r'^(?P<judge>[-_.\w]+)(/(?P<problem>[-_.\w]+))(/(?P<case>[-_.\w]+))?$', target)

        judge = result['judge']
        problem = result['problem']
        case = result['case']

        return judge, problem, case


class CommandList(BaseCommand):
    HELP_MESSAGE = "$ python pca.py list [judge_alias]/[problem_alias]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 1:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        try:
            judge, problem, __ = self.slash_separated_values(args[0])
        except TypeError:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

        self._judge = judge
        self._problem = problem

    def run(self):
        try:
            problem = ProblemFactory.load(self._judge, self._problem)
            print(problem)
            for case_id, case_options in problem.cases.items():
                print('  {}: {}'.format(case_id, case_options['options']))

        except FileNotFoundError:
            print('Problem Not Found')


class CommandCreate(BaseCommand):
    HELP_MESSAGE = "$ python pca.py create [judge_id]/[problem_id] [judge_alias]/[problem_alias]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 2:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        try:
            judge_id, problem_id, __ = self.slash_separated_values(args[0])
        except TypeError:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

        try:
            judge_alias, problem_alias, __ = self.slash_separated_values(args[1])
        except TypeError:
            self.display_help_message('Invalid Parameter: {}'.format(args[1]))
            raise InvalidCommandError

        self._judge_id = judge_id
        self._problem_id = problem_id

        self._judge_alias = judge_alias
        self._problem_alias = problem_alias

    def run(self):
        try:
            ProblemFactory.create(self._judge_id, self._problem_id, self._judge_alias, self._problem_alias)
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

        try:
            judge, problem, case = self.slash_separated_values(args[0])
        except TypeError:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

        self._judge = judge
        self._problem = problem
        self._case = case
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
                problem.run_all(save_output=self._save_output, detailed_output=self._detailed_output)

        except FileNotFoundError:
            print('Problem Not Found')


class CommandSkipCase(BaseCommand):
    HELP_MESSAGE = "$ python pca.py skipcase [judge_alias]/[problem_alias]/[case_id]"

    def __init__(self, *args):
        super().__init__(*args)
        if len(args) != 1:
            self.display_help_message('Too many Parameters: {}'.format(self._args))
            raise InvalidCommandError

        try:
            judge, problem, case = self.slash_separated_values(args[0])
        except TypeError:
            self.display_help_message('Invalid Parameter: {}'.format(args[0]))
            raise InvalidCommandError

        self._judge = judge
        self._problem = problem
        self._case = case

    def run(self):
        try:
            problem = ProblemFactory.load(self._judge, self._problem)

            if 'skip' in problem.cases[self._case]['options']:
                problem.cases[self._case]['options'].remove('skip')
            else:
                problem.cases[self._case]['options'].append('skip')

            problem.save()

            print(problem)
            for case_id, case_options in problem.cases.items():
                if case_id == self._case:
                    print(' *{}: {}'.format(case_id, case_options['options']))
                else:
                    print('  {}: {}'.format(case_id, case_options['options']))

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
    
    $ python pca.py create <judge_id>/<problem_id> <judge_alias>/<problem_alias>
    
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
