import sys

from instld.module.command_executer import CommandExecuter


def run_python(args, logger, catch_output):
    all_args = [sys.executable, *args]

    executer = CommandExecuter(all_args, catch_output=catch_output, logger=logger)
    executer.run()
