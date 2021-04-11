from os import environ
import base64

def env(name, fallback=None, parser=None):
    """
    Returns the specified environment variable.
    If it is not set, it returns the fallback value (if set) or raise an exception.
    If the parser is specified, it will call the parser with the environment value as argument.

    Example
    ----
    my_value = env('MY_VALUE', 300, int)
    """
    if name in environ:
        val = environ[name]
    elif fallback is not None:
        val = fallback
    else:
        raise Exception(f"Environment variable {name} must present")
    return parser(val) if parser else val


def periodic(scheduler, interval, action, actionargs=()):
    """
    A method for scheduling events to run every interval instead of only once.
    """
    scheduler.enter(interval, 1, periodic,
                    (scheduler, interval, action, actionargs))
    action(*actionargs)


def tob64(x):
    return base64.b64encode(x.encode('utf8')).decode('utf8')


def fromb64(x):
    return base64.b64decode(x.encode('utf8')).decode('utf8')
