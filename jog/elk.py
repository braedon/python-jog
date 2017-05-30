from datetime import datetime, tzinfo, timedelta

# Build our own UTC tzinfo, since datetime.timezone.utc doesn't
# exist pre 3.2 and we want to support 2.x

ZERO = timedelta(0)


class UTC(tzinfo):
    def utcoffset(self, dt):
        return ZERO

    def tzname(self, dt):
        return "UTC"

    def dst(self, dt):
        return ZERO


utc = UTC()


# Elasticsearch only supports a single type mapping for
# all elements in a list. Unless we are sure all elements
# in a list will encode to a single json type, normalise
# them to strings.
def clean_list(lst):
    non_null_lst = [i for i in lst if i is not None]
    if not non_null_lst:
        # List has no non-null elements, so safe
        return lst

    first_element = non_null_lst[0]

    # List is all strings - don't need to convert it
    if isinstance(first_element, (str,)) and \
       all([isinstance(i, (str,)) for i in non_null_lst[1:]]):
        return lst

    # List is all numbers - don't need to convert it
    elif isinstance(first_element, (int, float)) and \
            all([isinstance(i, (int, float)) for i in non_null_lst[1:]]):
        return lst

    # List is all booleans - don't need to convert it
    elif isinstance(first_element, (bool,)) and \
            all([isinstance(i, (bool,)) for i in non_null_lst[1:]]):
        return lst

    return [str(i) if i is not None else i for i in lst]


def clean(o):
    if isinstance(o, (list, tuple)):
        return clean_list(o)
    elif isinstance(o, (dict,)):
        return {k: clean(v) for k, v in o.items()}
    else:
        return o


def format_log(log_dict):

    created_timestamp = log_dict.pop('created')
    log_dict.update({
        '@version': 1,
        '@timestamp': datetime.fromtimestamp(created_timestamp, tz=utc).isoformat()
    })

    # Drop some fields we don't need:
    #  - asctime, msecs: we have formatted the timestamp in @timestamp
    #  - exec_info: we'll keep the formatted exc_text version
    for field in ['asctime', 'msecs', 'exc_info']:
        if field in log_dict:
            del log_dict[field]

    return clean(log_dict)
