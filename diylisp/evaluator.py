# -*- coding: utf-8 -*-

from types import Environment, LispError, Closure
from ast import is_boolean, is_atom, is_symbol, is_list, is_closure, is_integer
from asserts import assert_exp_length, assert_valid_definition, assert_boolean
from parser import unparse

"""
This is the Evaluator module. The `evaluate` function below is the heart
of your language, and the focus for most of parts 2 through 6.

A score of useful functions is provided for you, as per the above imports, 
making your work a bit easier. (We're supposed to get through this thing 
in a day, after all.)
"""

def evaluate(ast, env):
    """Evaluate an Abstract Syntax Tree in the specified environment."""

    if is_boolean(ast):
      return ast
    if is_integer(ast):
      return ast
    if is_list(ast):
      name = ast[0]
      fn   = forms[name] if name in forms else None

      if fn:
        return fn(ast[1:], env)
      else:
        raise NotImplementedError("Unrecognized symbol: %s" % ast[0])

forms = {
  "+"     : lambda ast, env: assert_int(ast[0], env) + assert_int(ast[1], env)
, "-"     : lambda ast, env: assert_int(ast[0], env) - assert_int(ast[1], env)
, "/"     : lambda ast, env: assert_int(ast[0], env) / assert_int(ast[1], env)
, "*"     : lambda ast, env: assert_int(ast[0], env) * assert_int(ast[1], env)
, ">"     : lambda ast, env: assert_int(ast[0], env) > assert_int(ast[1], env)
, "mod"   : lambda ast, env: assert_int(ast[0], env) % assert_int(ast[1], env)
, "eq"    : lambda ast, env: eq(ast[0], ast[1], env)
, "atom"  : lambda ast, env: is_atom(evaluate(ast[0], env))
, "quote" : lambda ast, env: ast[0]
}

def assert_int(x, env):
  x = evaluate(x, env)

  if is_integer(x):
    return x
  else:
    raise LispError("Expected integer but got: %s" % x)

def eq(a, b, env):
  a = evaluate(a, env)
  if not is_atom(a):
    return False

  b = evaluate(b, env)
  if not is_atom(b):
    return False

  return a == b