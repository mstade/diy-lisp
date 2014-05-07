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

    if is_atom(ast):
      return env.lookup(ast) if is_symbol(ast) else ast
    else:
      val = ast[0]

      if is_symbol(val):
        if val in forms:
          return forms[val](ast[1:], env)
        else:
          val = env.lookup(val)

      if is_closure(val):
        return apply(val, ast[1:], env)
      elif is_list(val):
        return evaluate([evaluate(val, env)] + ast[1:], env)
      else:
        raise LispError("%s is not a function." % unparse(val))

def math(op):
  def guard(ast, env):
    assert_exp_length(ast, 2)
    a = assert_int(ast[0], env)
    b = assert_int(ast[1], env)

    return op(a, b)

  return guard

def assert_int(x, env):
  x = evaluate(x, env)

  if is_integer(x):
    return x
  else:
    raise LispError("Expected integer but got: %s" % x)

def eq(ast, env):
  assert_exp_length(ast, 2)
  
  a = evaluate(ast[0], env)
  if not is_atom(a):
    return False

  b = evaluate(ast[1], env)
  if not is_atom(b):
    return False

  return a == b

def cond(ast, env):
  assert_exp_length(ast, 3)

  if evaluate(ast[0], env):
    return evaluate(ast[1], env)
  else:
    return evaluate(ast[2], env)

def defn(ast, env):
  assert_valid_definition(ast)
  env.set(ast[0], evaluate(ast[1], env))

def fn(ast, env):
  if len(ast) != 2:
      raise LispError("Wrong number of arguments for function definition: %s" % len(ast))

  params = ast[0]

  if not isinstance(params, list):
      raise LispError("Parameters must be a list, got: %s" % unparse(params))
  else:
    for p in params:
      if not isinstance(p, str):
        raise LispError("Parameter must be a symbol, got: %s" % unparse(p))

  body = ast[1]

  return Closure(env, params, body)

def apply(closure, args, env):
  variables = {}

  if len(args) != len(closure.params):
    raise LispError("wrong number of arguments, expected %s got %s" % (len(closure.params), len(args)))

  for i, key in enumerate(closure.params):
    variables[key] = evaluate(args[i], env)

  return evaluate(closure.body, closure.env.extend(variables))

forms = {
  "+"      : math(lambda a, b: a + b)
, "-"      : math(lambda a, b: a - b)
, "/"      : math(lambda a, b: a / b)
, "*"      : math(lambda a, b: a * b)
, ">"      : math(lambda a, b: a > b)
, "mod"    : math(lambda a, b: a % b)
, "if"     : cond
, "eq"     : eq
, "atom"   : lambda ast, env: is_atom(evaluate(ast[0], env))
, "quote"  : lambda ast, env: ast[0]
, "lambda" : fn
, "define" : defn
}