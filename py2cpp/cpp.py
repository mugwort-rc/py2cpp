# -*- coding: utf-8 -*-

import enum

class Type(enum.Enum):
    Builder = 0
    Block = 1
    Expr = 2
    Stmt = 4
    arguments = 2048


INDENT = " " * 4


class Base(object):
    def __init__(self, type):
        self.type = type

    def add_literal(self, literal):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError


class CodeStatement(Base):
    def __init__(self, stmt):
        super(CodeStatement, self).__init__(Type.Stmt)
        self.stmt = stmt


class Expr(CodeStatement):
    def build(self):
        return "{};".format(self.stmt.build())


class CodeExpression(Base):
    def __init__(self):
        super(CodeExpression, self).__init__(Type.Expr)


class BoolOp(CodeExpression):
    def __init__(self, op, values):
        self.op = op
        self.values = values

    def build(self):
        values = []
        for value in self.values:
            if isinstance(value, BoolOp):
                values.append("({})".format(value.build()))
            else:
                values.append(value.build())
        return " {} ".format(self.op).join(values)


class BinOp(CodeExpression):
    def __init__(self, left, op, right):
        super(BinOp, self).__init__()
        self.left = left
        self.op = op
        self.right = right

    def build(self):
        return " ".join([self.left.build(), self.op, self.right.build()])


class UnaryOp(CodeExpression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def build(self):
        operand = self.operand.build()
        if isinstance(self.operand, BoolOp):
            operand = "({})".format(operand)
        return "{}{}".format(self.op, operand)


class Lambda(CodeExpression):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def build(self):
        args = self.args.build()
        body = self.body.build()
        return "[&]({}) -> auto {{ return {}; }}".format(args, body)


class IfExp(CodeExpression):
    def __init__(self, test, body, orelse):
        self.test = test
        self.body = body
        self.orelse = orelse

    def build(self):
        test = self.test.build()
        body = self.body.build()
        orelse = self.orelse.build()
        return "(({}) ? ({}) : ({}))".format(test, body, orelse)


class Call(CodeExpression):
    def __init__(self, func, args=[], keywords=[], starargs=None, kwargs=None):
        self.func = func
        self.args = args
        self.keywords = keywords
        self.starargs = starargs
        self.kwargs = kwargs

    def build(self):
        args = ", ".join([x.build() for x in self.args])
        return "{}({})".format(self.func.build(), args)


class Num(CodeExpression):
    def __init__(self, n):
        super(Num, self).__init__()
        self.n = n

    def build(self):
        return "{}".format(self.n)


class Attribute(CodeExpression):
    def __init__(self, value, attr):
        super(Attribute, self).__init__()
        self.value = value
        self.attr = attr

    def build(self):
        return "{}.{}".format(self.value.build(), self.attr)


class Name(CodeExpression):
    def __init__(self, id):
        super(Name, self).__init__()
        self.id = id

    def build(self):
        return self.id


class arguments(Base):
    def __init__(self, args, vararg, kwarg, defaults):
        self.args = args
        self.vararg = vararg
        self.kwarg = kwarg
        self.defaults = defaults
        self.types = {}

    def get_arg_names(self):
        return [x.build() for x in self.args]

    def get_arg_values(self):
        return [x.build() for x in self.defaults]

    def set_arg_type(self, name, type):
        assert name in self.get_arg_names()
        self.types[name] = type

    def build(self):
        types = dict(self.types)
        names = self.get_arg_names()
        values = self.get_arg_values()
        for name in names:
            if name not in types:
                types[name] = "int"
        start = len(names) - len(values)
        args = []
        for i, name in enumerate(names):
            if i < start:
                args.append("{} {}".format(types[name], name))
            else:
                value = values[i - start]
                args.append("{} {}={}".format(types[name], name, value))
        return ", ".join(args)


#
# for C++ syntax special case
#

class CppScope(Attribute):
    def build(self):
        return "{}::{}".format(self.value.build(), self.attr)
