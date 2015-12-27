# -*- coding: utf-8 -*-

import enum

class Type(enum.Enum):
    Builder = 0
    Block = 1
    Expr = 2
    Stmt = 4


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


class BinOp(CodeExpression):
    def __init__(self, left, op, right):
        super(BinOp, self).__init__()
        self.left = left
        self.op = op
        self.right = right

    def build(self):
        return " ".join([self.left.build(), self.op, self.right.build()])


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


#
# for C++ syntax special case
#

class CppScope(Attribute):
    def build(self):
        return "{}::{}".format(self.value.build(), self.attr)
