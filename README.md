# INSTALLED: the simplest package management from the source code

[![codecov](https://codecov.io/gh/pomponchik/installed/branch/master/graph/badge.svg)](https://codecov.io/gh/pomponchik/installed)

Thanks to this package, it is very easy to manage the lifecycle of packages directly from the code.

Install [it](https://pypi.org/project/instld/):

```bash
pip install instld
```

And use as in this example:

```python
import installed


with installed('polog'):
  from polog import log, config, file_writer

  config.add_handlers(file_writer())

  log('some message!')
```

This code installs the [polog](https://github.com/pomponchik/polog) package, imports the necessary objects from there and displays a message. At the end of the program, there will be no excess garbage left in the system. This way you can easily try different packages without bothering with their installation and subsequent removal.
