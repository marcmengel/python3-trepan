"""Unit test for trepan.inout.input"""
import os.path as osp
import pytest

from trepan.inout.input import DebuggerUserInput

srcdir = osp.abspath(osp.dirname(__file__))

@pytest.mark.skip(reason="input handling has changed with removing 'raw'")
def test_DebuggerInput():
    cmdhelper_file = osp.join(srcdir, "..", "cmdhelper.py")
    inp = DebuggerUserInput(cmdhelper_file)
    assert isinstance(
        inp, DebuggerUserInput
    ), "Should have gotten a DebuggerUserInput object back"
    line = inp.readline()
    assert "# -*- coding: utf-8 -*-" == line
    inp.close()
    # Should be okay
    inp.close()
    return
