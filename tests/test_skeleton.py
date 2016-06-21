#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from classloadgrapher.skeleton import fib

__author__ = "menassezmengesha"
__copyright__ = "menassezmengesha"
__license__ = "new-bsd"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
