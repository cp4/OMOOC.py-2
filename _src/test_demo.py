#!/usr/bin/python
# -*- coding: utf-8 -*-
import nose
from nose.tools import assert_equals
from demo import hello


def test_default():
    assert hello() == "Hollo World!-)"
def test_put_foo():
    assert_equals(hello('foo'),
                        "foo" ) 

if __name__ == '__main__':
    nose.runmodule()

