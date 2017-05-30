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

Then log as normal:
```
logging.info('foo')
logging.info('foo %s', 'bar')
logging.info('foo %(baz)s', {'baz': 'bar'})
logging.info('foo %(baz)s', {'baz': 'bar'}, extra={'ekki': 'ptang'})
```

Or log an arbitrary dict:
```
logging.info({'foo': 'bar'})
```

# Output Format
Here's an example of a simple log and its output:
```
logging.info('foo')
```
```
{
    "@timestamp": "2017-05-30T11:25:51.168769+00:00",
    "@version": 1,
    "filename": "test.py",
    "funcName": "<module>",
    "levelname": "INFO",
    "levelno": 20,
    "lineno": 56,
    "log": "[2017-05-30 23:25:51,168] __main__.INFO MainThread test.<module> test.py:56 foo",
    "message": "foo",
    "message_format": "foo",
    "module": "test",
    "name": "__main__",
    "pathname": "test.py",
    "process": 7476,
    "processName": "MainProcess",
    "relativeCreated": 7.751226425170898,
    "thread": 139963963160320,
    "threadName": "MainThread"
}
```
Note that the output has been pretty-printed for ease of examination - each log Json object is actually output on a single line.

The Json objects produced are primarily a conversion of LogRecords into dicts, which are then rendered as Json. See the [official docs](https://docs.python.org/3/library/logging.html#logrecord-attributes) for details on fields included in a LogRecord. Note that the logging system will merge a `extra` dict into the LogRecord before it is passed to JogFormatter, so `extra` fields are treated as part of the LogRecord.

After the conversion of LogRecord to dict a number of transformations are applied.

## String Messages
A `msg` string is formatted using the `args` (if provided), and the result is put in the `message` field. The unformatted `msg` is put in `message_format`, and the `args` in `message_args`. An unstructured "traditional" log is also created using the `fmt` used to create the JogFormatter, and put in the `log` field:
```
logging.info('foo %s', 'bar')
```
```
{
    ...
    "message": "foo bar",
    "message_format": "foo %s",
    "message_args": ["bar"],
    "log": "[2017-05-30 22:03:48,217] __main__.INFO MainThread test.<module> test.py:45 foo bar",
    ...
}
```

If keyword formatting is used, the arguments dict is put in `message_kwargs` instead:
```
logging.info('foo %(baz)s', {'baz': 'bar'})
```
```
{
    ...
    "message": "foo bar",
    "message_format": "foo %(baz)s",
    "message_kwargs": {"baz": "bar"},
    "log": "[2017-05-30 22:03:48,217] __main__.INFO MainThread test.<module> test.py:45 foo bar",
    ...
}
```

## Dict Messages
A `msg` dict is merged straight into the log dict. Note that this will override any existing fields from the LogRecord (including fields from `extra`) with the same name.
```
logging.info({'foo': 'bar'})
```
```
{
    ...
    "foo": "bar",
    ...
}
```

No formatting is done, so attempting to provide `args` along with a dict `msg` will result in a logging error.
```
logging.info({'foo': 'bar'}, 'baz')  # results in a logging error
```

## Exceptions
If a LogRecord contains a `exc_info`, the exception is rendered and put into the `exc_text` field.
```
try:
    raise Exception('Foo!')
except Exception:
    logging.exception('bar')
```
```
{
    ...
    "exc_text": "Traceback (most recent call last):\n  File \"test.py\", line 51, in <module>\n    raise Exception('Foo!')\nException: Foo!",
    ...
}
```

## Post Processing Functions
JogFormatter takes a keyword argument `fn`, which is a function take takes a log dict (produced as described above) and returns the final dict to be rendered as Json, allowing arbitrary changes to be made before the log is written out.

By default, the provided `jog.elk.format_log` function is used. This function makes a number of changes to make the final Json suitable for ingestion into the ELK centralised logging system.

The `@version` field is set to `1`, and the `created` timestamp field is removed, converted to ISO format, and put in `@timestamp`. `asctime` and `msecs` are removed as they are not needed with `@timestamp` set. `exc_info` is also removed, as no special formatting is done with it, and `exc_text` is available.

Finally, the dict is cleaned to avoid (statelessly detectable) mapping conflicts in Elasticsearch. Specifically, if a list or tuple's contents are not homogenously a basic Json type (None, str, int|float, bool), the (non None) contents are converted to strings.
```
log.info('foo %(baz)s', {'baz': ['bar', 0, None]})
```
```
{
    ...
    "@version": 1,
    "@timestamp": "2017-05-30T11:34:31.901264+00:00",
    "message": "foo ['bar', 0, None]",
    "message_kwargs": {"baz": ["bar", "0", null]},
    ...
}
```

## Json Encoding
The final log dict is rendered as Json using the standard `json` library. Unencodable objects are automatically converted to strings to avoid losing logs when they are logged by mistake.

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
