# -*- coding: utf-8 -*-
#   Copyright (C) 2008-2010, 2013-2015, 2020-2021, 2024
#   Rocky Bernstein <rocky@gnu.org>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

import inspect
import os
from glob import glob
from types import CodeType
from typing import Any


def option_set(options: dict, value, default_options) -> Any:
    """
    If ``value`` is found in ``options``, return that, otherwise return the value
    from ``defaulit_options``.
    """
    # Yes, there is probably some fancy dictionary merge operation, that will do this,
    # as a one-shot but this code is simple and clear.
    if not options or value not in options:
        return default_options.get(value)
    else:
        return options.get(value)
    return None  # Not reached


def bool2YN(b: bool) -> str:
    """
    Turn a bool into the string "Y" or "N".
    """
    return "Y" if b else "N"


def wrapped_lines(msg_part1: str, msg_part2: str, width: int) -> str:
    """
    if ``msg_part1`` concatenated with ``msg_part2`` is larger than
    ``width`` then concatenate the strings with a new line and tab inserted
    between the strings. Otherwise, just concatenate with a space between the
    two strings.
    """
    if len(msg_part1) + len(msg_part2) + 1 > width:
        return msg_part1 + "\n\t" + msg_part2
    else:
        return msg_part1 + " " + msg_part2


def pretty_modfunc_name(s) -> str:
    if isinstance(s, CodeType):
        return f"{s.co_name}()"
    elif inspect.isfunction(s):
        return f"{s.__name__}()"
    elif str(s).startswith("<"):
        # FIXME:
        # Pick replace with something more custom to modname?
        return str(s)
    else:
        return str(s) + "()"


def pyfiles(callername, level=2):
    "All python files caller's dir without the path and trailing .py"
    d = os.path.dirname(callername)
    # Get the name of our directory.
    # A glob pattern that will get all *.py files but not __init__.py
    glob(os.path.join(d, "[a-zA-Z]*.py"))
    py_files = glob(os.path.join(d, "[a-zA-Z]*.py"))
    return [os.path.basename(filename[0:-3]) for filename in py_files]


# Demo it
if __name__ == "__main__":
    TEST_OPTS = {"a": True, "b": 5, "c": None}

    def get_option(key):
        return option_set(opts, key, TEST_OPTS)

    opts = {"d": 6, "a": False}
    for opt in ["a", "b", "c", "d"]:
        print(opt, get_option(opt))
        pass
    for b in [True, False]:
        print(bool2YN(b))
    pass

    print(wrapped_lines("hi", "there", 80))
    print(wrapped_lines("hi", "there", 5))
    print(pyfiles(__file__))
    print(pretty_modfunc_name(pretty_modfunc_name.__code__))
    print(pretty_modfunc_name(pyfiles))
    pass
