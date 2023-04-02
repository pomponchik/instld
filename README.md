# INSTALLED: the simplest package management from the source code

Thanks to this package, it is very easy to manage the lifecycle of packages directly from the code.


Install it:

```bash
pip install installed
```

And use as in this example:

```python
import installed


with installed('polog'):
  from polog import log, config, file_writer

  config.add_handlers(file_writer())

  log('some message!')
```

This code installs the polog package, imports the necessary objects from there and displays a message. At the end of the program, there will be no excess garbage left in the system. This way you can easily try different packages without bothering with their installation and subsequent removal.
