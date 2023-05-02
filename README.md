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
  module = context.import_here('some_module')
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
