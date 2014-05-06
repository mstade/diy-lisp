# -*- coding: utf-8 -*-

"""
This module holds some types we'll have use for along the way.

It's your job to implement the Closure and Environment types.
The LispError class you can have for free :)
"""

class LispError(Exception): 
    """General lisp error class."""
    pass

class Closure:
    
    def __init__(self, env, params, body):
        raise NotImplementedError("DIY")

    def __str__(self):
        return "<closure/%d>" % len(self.params)

class Environment:

    def __init__(self, variables=None):
        self.variables = variables if variables else {}

    def lookup(self, symbol):
        if symbol in self.variables:
            return self.variables[symbol]
        else:
            raise LispError("Undefined symbol: %s" % symbol)

    def extend(self, variables):
        d = self.variables.copy()
        d.update(variables if variables else {})
        return Environment(d)

    def set(self, symbol, value):
        if symbol in self.variables:
            raise LispError("Symbol %s is already defined" % symbol)
        else:
            self.variables[symbol] = value
