import argparse

from pypager.pager import Pager
from pypager.source import GeneratorSource

from logic import webhook

from collector.collection import AssignmentCollector
from prompt_toolkit import PromptSession
from prompt_toolkit.patch_stdout import patch_stdout
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import ValidationError, Validator
from prompt_toolkit.shortcuts import clear, prompt
from pyfiglet import Figlet

BANNER2 = Figlet(font='slant')  # Use Figlet for easier CLI banner rendering, easier to edit

PROMPT = '\U0001F3D7   '

COMMANDS = {
    'help': 'usage of each command',
    'duetoday': 'show assignments due today. q to exit, h for help',
    'duetomorrow': 'show assignments due tomorrow. q to exit, h for help',
    'alldue': 'show all assignments. q to exit, h for help',
    'pushms': 'push [today] or push [tomorrow] push assignments to ms teams',
    'pushe': 'pushe [today] or pushe [tomorrow] push assignments to email',
    'setreminder': 'add tomorrow\'s homework reminder to google calendar (Needs API key)',
    'clear': 'clear screen'
}


def parse_cmd(raw_cmd) -> tuple:
    """
    parse a command return command and arg list
    """
    command = raw_cmd.split(' ')[0].strip()
    if len(raw_cmd.split(' ')) == 1:
        return command, []
    if command in ['pushms', 'pushe']:
        # only one arg for these cmd s
        arguments = [raw_cmd.split(' ')[1].strip()]
        return command, arguments


def send_assignments(assignments):  # Generator needed by pypager
    for assignment in assignments:
        yield [("", '{}\n'.format(assignment))]


class CommandValidator(Validator):
    """
    validator for prompt_tool
    """

    def validate(self, document):
        text = document.text
        try:
            command, args_list = parse_cmd(text)
        except:
            command = ''
            args_list = []
        if command not in COMMANDS.keys():
            raise ValidationError(
                message=f'{command} is not a valid command.')
        if command in ['pushms', 'pushe']:
            if len(args_list) != 1:
                raise ValidationError(message='arg number mismatch expect 1.')


class CommandExecutor:

    def __init__(self):
        self.collector = AssignmentCollector()

    def execute(self, raw_cmd):
        command, arguments = parse_cmd(raw_cmd)
        if command == 'help':
            self.__help()
        elif command == 'duetoday':
            self.__due_today()
        elif command == 'duetomorrow':
            self.__due_tomorrow()
        elif command == 'alldue':
            self.__all_due()
        elif command == 'pushms':
            self.__push_ms(arguments[0])
        elif command == 'pushe':
            self.__push_e(arguments[0])
        elif command == 'setreminder':
            self.__add_to_calendar()
        elif command == 'clear':
            self.__clear()
        else:
            print("Command not available!")

    @classmethod
    def __help(cls):
        with patch_stdout():
            print("")
        for k, v in COMMANDS.items():
            with patch_stdout():
                print('{} : {}'.format(k, v))
        with patch_stdout():
            print("")

    @classmethod
    def __clear(cls):
        clear()

    def __due_today(self):
        assign = ["--------Due Today--------\n"]
        p = Pager()

        try:
            for item in self.collector.print_assignments(cmd='today'):
                assign.append(item)
                if "What is Due:" in item:
                    assign.append("\n-------------------")

            p.add_source(GeneratorSource(send_assignments(assign)))
            p.run()
        except EOFError:
            return

    def __due_tomorrow(self):
        assign = ["--------Due Tomorrow--------\n"]
        p = Pager()

        try:
            for item in self.collector.print_assignments(cmd='tomorrow'):
                assign.append(item)
                if "What is Due:" in item:
                    assign.append("\n-------------------")

            p.add_source(GeneratorSource(send_assignments(assign)))
            p.run()
        except EOFError:
            return

    def __all_due(self):
        assign = ["--------All Due--------\n"]
        p = Pager()
        try:
            for item in self.collector.print_assignments(cmd='all'):
                assign.append(item)
                if "What is Due:" in item:
                    assign.append("\n-------------------")

            p.add_source(GeneratorSource(send_assignments(assign)))
            p.run()
        except EOFError:
            print("Something went wrong...")

    def __push_ms(self, cmd):
        try:
            if webhook.WEBHOOK is None:
                webhook_user = prompt("Enter MS webhook: ")
                use_web = webhook_user
            else:
                use_web = webhook.WEBHOOK
            card_title = prompt("Enter custom card title: enter [n] for default: ")
            if card_title.lower() == 'n':
                card_title = None
            action = self.collector.push_to_ms(webhook=use_web, cmd=cmd, card_title=card_title)
            if action:
                action()
            else:
                print("")
        except EOFError:
            print("Something went wrong...")

    def __push_e(self, cmd):
        try:
            self.collector.push_email(cmd=cmd)
        except EOFError:
            return

    def __add_to_calendar(self):
        try:
            print("Creating Reminder...")
            reminder = self.collector.create_event()
            if reminder:
                print(reminder)
            else:
                reminder()
        except EOFError:
            print("Something Went wrong...")
            return


def main():
    print(BANNER2.renderText("IST 256 Reminders"))
    print(
        "Application will gather IST 256 Assignments. crtl + d to exit\n"
        "For Professors/TAs, you can Push these to MS Teams and email\n"
        "If no MS webhook is saved, it will need to be entered in manually\n")

    cmd_completer = WordCompleter(COMMANDS.keys(), True)
    cmd_validator = CommandValidator()
    session = PromptSession(completer=cmd_completer)
    executor = CommandExecutor()

    while True:
        try:
            cmd = session.prompt(PROMPT, validator=cmd_validator)
            executor.execute(cmd)
        except KeyboardInterrupt:
            continue
        except EOFError:
            break

    print('\nSee yah!\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CLI for assignment collection')
    args = parser.parse_args()
    main()