import sys
import subprocess


def run_python(args, logger):
    all_args = [sys.executable, *args]
    args_string_representation = " ".join(all_args)

    try:
        logger.info(f'The beginning of the execution of the command "{args_string_representation}".')
        subprocess.check_call(all_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info(f'The command "{args_string_representation}" has been executed.')

    except subprocess.CalledProcessError as e:
        logger.error(f'Error when executing the command "{args_string_representation}".')
        raise

    except Exception as e:
        logger.exception(f'Error when executing the command "{args_string_representation}".')
        raise
