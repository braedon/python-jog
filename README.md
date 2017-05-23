Jog: Python Json Structured Logging
====
Format your python logs as JSON objects, perfect for easy ingestion into centralised logging systems.

# Installation
Installation is pretty simple with pip:
```
> pip install jog
```

Depending on your system, you might need to use pip3 to install for Python 3 (ditto for any other pip commands):
```
> pip3 install jog
```

# Usage
Once installed, import the `JogFormatter` and configure the logging system to use it. e.g.:
```
import logging
from jog import JogFormatter

log_handler = logging.StreamHandler()
log_format = '[%(asctime)s] %(name)s.%(levelname)s %(threadName)s %(module)s.%(funcName)s %(filename)s:%(lineno)s %(message)s'
log_handler.setFormatter(JogFormatter(log_format))

root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(log_handler)
```

# Development
To install directly from the git repo, run the following in the root project directory:
```
> pip install .
```

The library can be installed in "editable" mode, using pip's `-e` flag. This allows you to test out changes without having to re-install.
```
> pip install -e .
```

Send me a PR if you have a change you want to contribute!
