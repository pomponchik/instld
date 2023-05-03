# INSTALLED: the simplest package management in runtime

[![Downloads](https://pepy.tech/badge/instld/month)](https://pepy.tech/project/instld)
[![Downloads](https://pepy.tech/badge/instld)](https://pepy.tech/project/instld)
[![codecov](https://codecov.io/gh/pomponchik/installed/branch/main/graph/badge.svg)](https://codecov.io/gh/pomponchik/installed)
[![Test-Package](https://github.com/pomponchik/installed/actions/workflows/coverage.yml/badge.svg)](https://github.com/pomponchik/installed/actions/workflows/coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/instld.svg)](https://pypi.python.org/pypi/instld)
[![PyPI version](https://badge.fury.io/py/instld.svg)](https://badge.fury.io/py/instld)

Thanks to this package, it is very easy to manage the lifecycle of packages directly from the code. In runtime.

- ⚡ You can use 2 different versions of the same library in the same program.
- ⚡ You can use incompatible libraries in the same project, as well as libraries with incompatible/conflicting dependencies.
- ⚡ It's easy to share written scripts. The script file becomes self-sufficient - the user does not need to install the necessary libraries.
- ⚡ The library does not leave behind "garbage". After the end of the program, no additional files remain in the system.


## Table of contents

- [**Quick start**](#quick-start)
- [**Imports**](#imports)
- [**Installing multiple packages**](#installing-multiple-packages)
- [**Options**](#options)
- [**Output and logging**](#output-and-logging)
- [**How does it work?**](#how-does-it-work)


## Quick start

Install [it](https://pypi.org/project/instld/):

```bash
pip install instld
```

And use as in this example:

```python
import installed


with installed('some_package') as context:
  import some_module
```

The above code downloads `some_package` and imports `some_module` from it.


## Imports

The context manager `installed` generates a context. While you are inside the context manager, you can import modules using the usual `import` command:

```python
with installed('some_package'):
  import some_module
```

However, there are cases when you need the module to be imported strictly from a given context. In this case, it is better to use the `import_here` method:

```python
with installed('some_package') as context:
  module = context.import_here('some_module')
```

The library provides isolation of various contexts among themselves, so in the second case, the module will be imported strictly from the context that you need.


## Installing multiple packages

You can install several packages by specifying their names separated by commas:

```python
with installed('package_1', 'package_2', 'package_3') as context:
  module_1 = context.import_here('module_1')
  module_2 = context.import_here('module_2')
  module_3 = context.import_here('module_3')
```

In this case, all packages will be installed in one context and you can import them all from there.

You can also create separate contexts for different packages:

```python
with installed('package_1') as context_1:
  with installed('package_2') as context_2:
    with installed('package_3') as context_3:
      module_1 = context_1.import_here('module_1')
      module_2 = context_2.import_here('module_2')
      module_3 = context_3.import_here('module_3')
```

In this case, each package was installed in its own independent context, and we import each module from the context where the corresponding package was installed.

This capability is very powerful. You can place libraries in different contexts that are incompatible with each other. You can also install different versions of the same library in neighboring contexts. Here's how it will work using the [Flask](https://flask.palletsprojects.com/) example:

```python
with installed('flask==2.0.2') as context_1:
    with installed('flask==2.0.0') as context_2:
        flask_1 = context_1.import_here('flask')
        flask_2 = context_2.import_here('flask')

        print(flask_1.__version__)  # 2.0.2
        print(flask_2.__version__)  # 2.0.0
```

> ⚠️ Keep in mind that although inter-thread isolation is used inside the library, working with contexts is not completely thread-safe. You can write code in such a way that two different contexts import different modules in separate threads at the same time. In this case, you may get paradoxical results. Therefore, it is recommended to additionally isolate with mutexes all cases where you import something from contexts in different threads.


## Options

You can use [any options](https://pip.pypa.io/en/stable/cli/pip_install/) available for `pip`. To do this, you need to slightly change the name of the option, replacing the hyphens with underscores, and pass it as an argument to `installed`. Here is an example of how using the `--index-url` option will look like:

```python
with installed('super_test_project==0.0.1', index_url='https://test.pypi.org/simple/'):
  import super_test
```

You cannot use options that tell `pip` where to install libraries.


## Output and logging

By default, you can see the output of the installation progress in the console:

```python
>>> with installed('flask'):
...     import flask
...
Collecting flask
  Using cached Flask-2.3.2-py3-none-any.whl (96 kB)
Collecting click>=8.1.3
  Using cached click-8.1.3-py3-none-any.whl (96 kB)
Collecting importlib-metadata>=3.6.0
  Using cached importlib_metadata-6.6.0-py3-none-any.whl (22 kB)
Collecting Jinja2>=3.1.2
  Using cached Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting Werkzeug>=2.3.3
  Using cached Werkzeug-2.3.3-py3-none-any.whl (242 kB)
Collecting itsdangerous>=2.1.2
  Using cached itsdangerous-2.1.2-py3-none-any.whl (15 kB)
Collecting blinker>=1.6.2
  Using cached blinker-1.6.2-py3-none-any.whl (13 kB)
Collecting zipp>=0.5
  Using cached zipp-3.15.0-py3-none-any.whl (6.8 kB)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.1.2-cp39-cp39-macosx_10_9_universal2.whl (17 kB)
Installing collected packages: zipp, MarkupSafe, Werkzeug, Jinja2, itsdangerous, importlib-metadata, click, blinker, flask
Successfully installed Jinja2-3.1.2 MarkupSafe-2.1.2 Werkzeug-2.3.3 blinker-1.6.2 click-8.1.3 flask-2.3.2 importlib-metadata-6.6.0 itsdangerous-2.1.2 zipp-3.15.0
```

If you don't want to see this output, pass the `catch_output` argument:

```python
>>> with installed('flask', catch_output=True):
...     import flask
...
>>>
```

In case of installation errors, you will get an `installed.errors.InstallingPackageError` exception. From the object of this exception, you can get `stdout` and `stderr` even if you have forbidden the output:

```python
from installed.errors import InstallingPackageError


try:
  with installed('some_wrong_pack', catch_output=True):
    import some_wrong_module
except InstallingPackageError as e:
  print(e.stdout)
  print(e.stderr)
```

Logging is also enabled by default for installing packages. You can see it if you configure logging correctly. In this case:

```python
import logging


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(),
    ]
)

with installed('flask', catch_output=True):
  import flask
```

... the logs will look something like this:

```
2023-05-02 13:47:56,752 [INFO] The beginning of the execution of the command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m venv /var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv".
2023-05-02 13:47:58,993 [INFO] The command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m venv /var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv" has been executed.
2023-05-02 13:47:58,993 [INFO] The beginning of the execution of the command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m pip install --target=/var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv/lib/python3.9/site-packages flask".
2023-05-02 13:48:01,052 [INFO] The command "/Users/pomponchik/Desktop/Projects/magic-action-runner/venv/bin/python3 -m pip install --target=/var/folders/54/p5qzzp9j65zckq9kd2k31t9c0000gn/T/tmpiajesk4s/venv/lib/python3.9/site-packages flask" has been executed.
```

The `INFO` [level](https://docs.python.org/3/library/logging.html#logging-levels) is used by default. For errors - `ERROR`.

## How does it work?

This package is essentially a wrapper for `venv` and `pip`.

When entering the context, a temporary folder is created using the [tempfile](https://docs.python.org/3/library/tempfile.html) library. Then it is added to [sys.path](https://docs.python.org/3/library/sys.html#sys.path), and after exiting the context, it is removed from there. To install the package in this particular temporary folder, the `--target` argument is passed to pip, indicating the path to it. Interaction with `pip` and `venv` occurs through [subprocesses](https://docs.python.org/3/library/subprocess.html).

The `import_here` method works by temporarily substituting [sys.path](https://docs.python.org/3/library/sys.html#sys.path) and [sys.modules](https://docs.python.org/3/library/sys.html#sys.modules). This is necessary so that the search for packages takes place only in the necessary directories.
