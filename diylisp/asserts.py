# -*- coding: utf-8 -*-

from types import LispError
from parser import unparse
from ast import is_boolean, is_symbol

def assert_exp_length(ast, length):
    if len(ast) > length:
        msg = "Malformed call, too many arguments: %s" % unparse(ast)
        raise LispError(msg)
    elif len(ast) < length:
        msg = "Malformed call, too few arguments: %s" % unparse(ast)
        raise LispError(msg)

def assert_valid_definition(d):
    if len(d) != 2:
        msg = "Wrong number of arguments for variable definition: %s" % d
        raise LispError(msg)
    elif not isinstance(d[0], str):
        msg = "Attempted to define non-symbol as variable: %s" % d
        raise LispError(msg)

def assert_boolean(p, exp=None):
    if not is_boolean(p):
        msg = "Boolean required, got '%s'. " % unparse(p)
        if exp is not None:
            msg += "Offending expression: %s" % unparse(exp)
        raise LispError(msg)

def assert_symbol(p, exp=None):
    if not is_symbol(p):
        msg = "Symbol required, got '%s'. " % unparse(p)
        if exp is not None:
            msg += "Offending expression: %s" % unparse(exp)
        raise LispError(msg)
