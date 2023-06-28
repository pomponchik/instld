import sys
import subprocess


def run_python(args, logger, catch_output, outputs):
    all_args = [sys.executable, *args]
    args_string_representation = " ".join(all_args)

    try:
        logger.info(f'The beginning of the execution of the command "{args_string_representation}".')
        result = subprocess.run(all_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout = result.stdout.decode('utf-8')
        stderr = result.stderr.decode('utf-8')
        outputs.append(stdout)
        outputs.append(stderr)
        if not catch_output:
            print(stdout, end='')
            print(stderr, end='')

        result.check_returncode()
        logger.info(f'The command "{args_string_representation}" has been executed.')

    except subprocess.CalledProcessError as e:
        logger.error(f'Error when executing the command "{args_string_representation}".')
        raise

    except Exception as e:
        logger.exception(f'Error when executing the command "{args_string_representation}".')
        raise
