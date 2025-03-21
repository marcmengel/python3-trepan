# -*- coding: utf-8 -*-
#
#   Copyright (C) 2009, 2012-2013, 2020, 2023-2024 Rocky Bernstein
#   <rocky@gnu.org>
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
"""Bytecode instruction routines"""

import re

from opcode import opname
from typing import Optional
from xdis import PYTHON_VERSION_TRIPLE, get_opcode_module

opcode_module = get_opcode_module(PYTHON_VERSION_TRIPLE)


def opname_at_code_offset(bytecode_bytes: bytes, offset: int) -> str:
    try:
        opcode = bytecode_bytes[offset]
    except IndexError:
        return "got IndexError"
    return opname[opcode]



def op_at_frame(frame, offset: Optional[int]=None, skip_cache=True):
    bytecode = frame.f_code.co_code
    if offset is None:
        offset = frame.f_lasti
    while skip_cache and offset != 0 and opname_at_code_offset(bytecode, offset) == "CACHE":
        offset -= 2
    return opname_at_code_offset(bytecode, offset)


def next_opcode(code, offset):
    """Return the next opcode and offset as a tuple. Tuple (-100,
    -1000) is returned when reaching the end."""
    n = len(code)
    while offset < n:
        op = code[offset]
        yield op, offset
        offset = offset + 2
        yield op, offset
        pass
    yield -100, -1000
    pass


def next_linestart(co, offset: int, count=1) -> int:
    code = co.co_code

    linestarts = dict(opcode_module.findlinestarts(co))
    n = len(code)
    # contains_cond_jump = False
    while offset < len(code):
        if offset in linestarts:
            count -= 1
            if 0 == count:
                return linestarts[offset]
            pass
        offset += 2

    return -1000


def stmt_contains_opcode(co, lineno, query_opname) -> bool:
    linestarts = dict(opcode_module.findlinestarts(co))
    code = co.co_code
    found_start = False
    offset = 0
    start_line = None
    for offset, start_line in list(linestarts.items()):
        if start_line == lineno:
            print("=" * 30)
            found_start = True
            break
        pass
    if not found_start:
        return False
    for op, offset in next_opcode(code, offset):
        linestart = linestarts.get(offset)
        if -1000 == offset or linestart and linestart != start_line:
            return False
        op_name = opname[op]
        # debug: print opname
        if query_opname == op_name:
            return True
        pass
    return False


_re_def_str = r"^\s*def\s"
_re_def = re.compile(_re_def_str)


def is_def_stmt(line: Optional[str], frame) -> bool:
    """Return True if we are looking at a def statement"""
    # Should really also check that operand of 'LOAD_CONST' is a code object
    return (
        line
        and _re_def.match(line)
        and op_at_frame(frame) == "LOAD_CONST"
        and stmt_contains_opcode(frame.f_code, frame.f_lineno, "MAKE_FUNCTION")
    )


_re_class = re.compile(r"^\s*class\s")


def is_class_def(line, frame):
    """Return True if we are looking at a class definition statement"""
    return (
        line
        and _re_class.match(line)
        and stmt_contains_opcode(frame.f_code, frame.f_lineno, "BUILD_CLASS")
    )


# Demo stuff above
if __name__ == "__main__":
    import inspect

    def sqr(x):
        return x * x

    frame = inspect.currentframe()
    co = frame.f_code
    lineno = frame.f_lineno
    print(
        "contains MAKE_FUNCTION %s"
        % stmt_contains_opcode(co, lineno - 4, "MAKE_FUNCTION")
    )
    print(
        f"contains MAKE_FUNCTION {stmt_contains_opcode(co, lineno, 'MAKE_FUNCTION')}"
    )

    print(f"op at frame: {op_at_frame(frame)}")
    print(f"op at frame, position 2: {op_at_frame(frame, 2)}")
    print(f"def statement: x=5?: {is_def_stmt('x=5', frame)}")
    # Not a "def" statement because frame is wrong spot
    print(is_def_stmt("def foo():", frame))

    class Foo:
        pass

    lineno = frame.f_lineno
    print(
        f"contains BUILD_CLASS {stmt_contains_opcode(co, lineno - 2, 'BUILD_CLASS')}"
    )
    print(f"contains BUILD_CLASS {stmt_contains_opcode(co, lineno, 'BUILD_CLASS')}")
    pass
