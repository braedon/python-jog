import json
import logging
from . import elk


class LoggingJSONEncoder(json.JSONEncoder):

    # We don't want to lose a log because it contains
    # a object we don't know how to encode. Instead,
    # convert it to a string.
    def default(self, o):
        return str(o)


class JogFormatter(logging.Formatter):

    def __init__(self, fmt=None, datefmt=None, style=None, fn=elk.format_log):
        self.fn = fn
        kwargs = {
            'fmt': fmt,
            'datefmt': datefmt
        }
        # Python2 logging.Formatter doesn't support the `style` parameter so
        # only pass it on if passed to us.
        if style:
            kwargs['style'] = style
        super(JogFormatter, self).__init__(**kwargs)

    def format(self, record):
        # Call this first as it changes the record, e.g. formatting exceptions.
        # For efficency's sake, we use these changes rather than performing
        # them ourselves.
        plain_text_log = super(JogFormatter, self).format(record)

        fields = record.__dict__.copy()

        field_updates = {}

        message_format = fields.pop('msg')
        # If the message is a dict use it directly
        if isinstance(message_format, (dict,)):
            field_updates.update(message_format)

        # Otherwise it's a normal log record, so we need to format it
        else:
            # Preserve the unformatted message string.
            # Useful for selecting selecting all instances of a log,
            # regardless of the variables substituted in.
            field_updates['message_format'] = message_format

            # The format args can be either args (list) or kwargs (dict)
            # so split into different fields to simplify handling later.
            if 'args' in fields:
                args = fields.pop('args')
                if isinstance(args, (dict,)):
                    field_updates['message_kwargs'] = args
                else:
                    field_updates['message_args'] = args

            # The formatted message itself
            field_updates['message'] = record.getMessage()

            # The full formatted non-structured log line.
            # Useful if you need to tail the logs.
            field_updates['log'] = plain_text_log

        log = fields
        log.update(field_updates)

        # Drop empty fields
        log = {k: v for k, v in log.items() if v}

        log = self.fn(log)

        return json.dumps(log, sort_keys=True, cls=LoggingJSONEncoder)
