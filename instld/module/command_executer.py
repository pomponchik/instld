import sys
from threading import Thread, Lock
from subprocess import Popen, PIPE

from instld.module.empty_logger import EmptyLogger
from instld.errors import RestartingCommandError, RunningCommandError


class CommandExecuter:
    def __init__(self, arguments, catch_output=True, logger=EmptyLogger()):
        self.arguments = arguments
        self.arguments_string_representation = ' '.join(self.arguments)
        self.catch_output = catch_output
        self.logger = logger
        self.stdout = []
        self.stderr = []
        self.running = False
        self.done = False
        self.lock = Lock()

    def run(self):
        """
        About reading from strout and stderr: https://stackoverflow.com/a/28319191/14522393
        """
        with self.lock:
            if self.done or self.running:
                raise RestartingCommandError('You cannot run the same command twice. To restart, create a new instance.')
            self.running = True

        self.logger.info(f'The beginning of the execution of the command "{self.arguments_string_representation}".')

        with Popen(self.arguments, stdout=PIPE, stderr=PIPE, bufsize=1, universal_newlines=True) as process:
            stderr_reading_thread = Thread(target=self.read_stderr, args=(process,))
            stderr_reading_thread.start()

            for line in process.stdout:
                self.stdout.append(line)
                if not self.catch_output:
                    print(line, end='')

            stderr_reading_thread.join()

        self.done = True
        self.running = False

        if process.returncode != 0:
            message = f'Error when executing the command "{self.arguments_string_representation}".'
            self.logger.error(message)
            exception = RunningCommandError(message)
            exception.stdout = ''.join(self.stdout)
            exception.stderr = ''.join(self.stderr)
            raise exception

        self.logger.info(f'The command "{self.arguments_string_representation}" has been executed.')

    def read_stderr(self, process):
        for line in process.stderr:
            self.stderr.append(line)
            if not self.catch_output:
                sys.stderr.write(line)
