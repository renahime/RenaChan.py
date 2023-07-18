import datetime
import platform
import socket
import sys

from .cogs import *
from .managers import *
from .tools import *
from .config import *
from .events import *
from .messages import *
from .setup import *


def version():
    return "v0.1"


def config_version():
    return "0.1"  # do not edit this!


def time():
    return datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")


def year():
    return str(datetime.datetime.now().year)


def copyright():
    if year() == "2023":
        return "© 2023 By Rena"
    else:
        return f"© 2023-{year()} By Rena"


def platform():
    return platform.system() + " " + platform.release()

def path():
    return sys.path
