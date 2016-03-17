"""Formulas are essentially for maths, like templates
callbacks/bind are for signals/late-binding
"""

import operator
import math
import numbers

def apply(f, ctx={}):
    if isinstance(f, Formula):
        return f.apply(ctx)
    return f

def isnumeric(n):
    return isinstance(n, numbers.Number)

def strict_apply(f, ctx={}):
    value = apply(f, ctx)
    if not isnumeric(value):
        raise ValueError('{} is not a number'.format(repr(value)))
    return value

class Formula:
    def apply(self, ctx):
        raise NotImplemented

ops = {
    'pos': (operator.pos, '+{}', 1),
    'neg': (operator.neg, '-{}', 1),
    'not': (operator.not_, '!{}', 1),
    'invert': (operator.invert, '~{}', 1),
    'abs': (operator.abs, 'abs({})', 1),
    'round': (round, 'round({})', 1),
    'floor': (math.floor, 'math.floor({})', 1),
    'ceil': (math.ceil, 'math.ceil({})', 1),
    'int': (int, 'int({})', 1),
    'float': (float, 'float({})', 1),

    'add': (operator.add, '({} + {})', 2),
    'sub': (operator.sub, '({} - {})', 2),
    'mul': (operator.mul, '({} * {})', 2),
    'floordiv': (operator.floordiv, '({} // {})', 2),
    'truediv': (operator.truediv, '({} / {})', 2),
    'mod': (operator.mod, '({} % {})', 2),
    'pow': (operator.pow, '({} ** {})', 2),
    'eq': (operator.eq, '({} == {})', 2),
    'ne': (operator.ne, '({} != {})', 2),
    'lt': (operator.lt, '({} < {})', 2),
    'le': (operator.le, '({} <= {})', 2),
    'gt': (operator.gt, '({} > {})', 2),
    'ge': (operator.ge, '({} >= {})', 2),
    'and': (operator.and_, '({} & {})', 2),
    'or': (operator.or_, '({} | {})', 2),
    'xor': (operator.xor, '({} ^ {})', 2),
    'lshift': (operator.lshift, '({} << {})', 2),
    'rshift': (operator.rshift, '({} >> {})', 2),
}

def set_op(op_func, op_str, op_type):
    if op_type == 1:
        def op(self):
            return FUnOp(op_func, self, op_str)
        setattr(Formula, '__{}__'.format(name), op)
    elif op_type == 2:
        def op(self, rhs):
            return FBinOp(op_func, self, rhs, op_str)
        def rop(self, lhs):
            return FBinOp(op_func, lhs, self, op_str)
        setattr(Formula, '__{}__'.format(name), op)
        setattr(Formula, '__r{}__'.format(name), rop)

for name, op in ops.items():
    set_op(*op)

class FUnOp(Formula):
    def __init__(self, op, v, fmt='{} ¤ {}'):
        self.op = op
        self.v = v
        self.fmt = fmt

    def apply(self, ctx):
        return self.op(apply(self.v, ctx))

    def __repr__(self):
        return self.fmt.format(repr(self.v))

class FBinOp(Formula):
    def __init__(self, op, a, b, fmt='¤{}'):
        self.op = op
        self.a = a
        self.b = b
        self.fmt = fmt

    def apply(self, ctx):
        a = apply(self.a, ctx)
        b = apply(self.b, ctx)
        return self.op(a, b)

    def __repr__(self):
        return self.fmt.format(repr(self.a), repr(self.b))

class Var(Formula):
    def __init__(self, name):
        self.name = name

    def apply(self, ctx):
        if self.name in ctx:
            return ctx[self.name]
        return self

    def __repr__(self):
        return self.name

class Cond(Formula):
    def __init__(self, predicate, then, else_):
        self.predicate = predicate
        self.then = then
        self.else_ = else_

    def apply(self, ctx):
        p = apply(self.predicate, ctx)
        if not isnumeric(p):
            return Cond(p, apply(self.then, ctx), apply(self.else_, ctx))
        if p:
            return apply(self.then, ctx)
        return apply(self.else_, ctx)

    def __repr__(self):
        return '({} if {} else {})'.format(self.then, self.predicate, self.else_)
