# -*- coding: utf-8 -*-

import enum

class Type(enum.Enum):
    Builder = 0
    Block = 1
    Expr = 2
    Stmt = 4
    arguments = 2048


INDENT = " " * 4


class BuildContext(object):
    def __init__(self):
        self.indent_level = 0

    def __enter__(self):
        self.indent_level += 1

    def __exit__(self, exc_type, exc_value, traceback):
        self.indent_level -= 1
        return False if exc_type else True

    def indent(self):
        return INDENT * self.indent_level


class Base(object):
    def __init__(self, type):
        self.type = type

    def add_literal(self, literal):
        raise NotImplementedError

    def build(self, ctx):
        """
        :type ctx: BuildContext
        """
        raise NotImplementedError


class CodeStatement(Base):
    def __init__(self, stmt):
        super(CodeStatement, self).__init__(Type.Stmt)
        self.stmt = stmt


class FunctionDef(CodeStatement):
    def __init__(self, name, args, body):
        super(FunctionDef, self).__init__(body)
        self.name = name
        self.args = args

    def build(self, ctx):
        with ctx:
            body = [x.build(ctx) for x in self.stmt]
        return "\n".join([
            "{}void {}({}) {{".format(
                ctx.indent(),
                self.name,
                self.args.build(ctx),
            ),
            "\n".join(body),
            ctx.indent() + "}",
        ])


class ClassDef(CodeStatement):
    def __init__(self, name, bases, body, **kwargs):
        super(ClassDef, self).__init__(body)
        self.name = name
        self.bases = bases
        self.keywords = kwargs.get("keywords", [])

    def build(self, ctx):
        with ctx:
            body = [x.build(ctx) for x in self.stmt]
        return "\n".join([
            "{}class {}{} {{".format(
                ctx.indent(),
                self.name,
                " : {}".format(", ".join(["public " + x.build(ctx) for x in self.bases])) if self.bases else "",
            ),
            "\n".join(body),
            ctx.indent() + "};",
        ])


class Return(CodeStatement):
    def __init__(self, value):
        self.value = value

    def build(self, ctx):
        if self.value:
            return ctx.indent() + "return {};".format(self.value.build(ctx))
        else:
            return ctx.indent() + "return;"


class Assign(CodeStatement):
    def __init__(self, targets, value):
        self.targets = targets
        self.value = value

    def build(self, ctx):
        return ctx.indent() + "{} = {};".format(
            " = ".join([x.build(ctx) for x in self.targets]),
            self.value.build(ctx)
        )


class AugAssign(CodeStatement):
    def __init__(self, target, op, value):
        self.target = target
        self.op = op
        self.value = value

    def build(self, ctx):
        return ctx.indent() + "{} {}= {};".format(
            self.target.build(ctx),
            self.op,
            self.value.build(ctx)
        )


class While(CodeStatement):
    def __init__(self, test, body, orelse):
        super(While, self).__init__(body)
        self.test = test
        self.orelse = orelse

    def build(self, ctx):
        with ctx:
            body = [x.build(ctx) for x in self.stmt]
        # TODO: orelse
        return "\n".join(["{}while ({}) {{".format(
                ctx.indent(),
                self.test.build(ctx)
            ),
            "\n".join(body),
            ctx.indent() + "}",
        ])


class Expr(CodeStatement):
    def build(self, ctx):
        return ctx.indent() + "{};".format(self.stmt.build(ctx))


class Pass(CodeStatement):
    def __init__(self):
        pass

    def build(self, ctx):
        return ""


class Break(CodeStatement):
    def __init__(self):
        pass

    def build(self, ctx):
        return ctx.indent() + "break;"


class Continue(CodeStatement):
    def __init__(self):
        pass

    def build(self, ctx):
        return ctx.indent() + "continue;"


class CodeExpression(Base):
    def __init__(self):
        super(CodeExpression, self).__init__(Type.Expr)


class BoolOp(CodeExpression):
    def __init__(self, op, values):
        self.op = op
        self.values = values

    def build(self, ctx):
        values = []
        for value in self.values:
            if isinstance(value, BoolOp):
                values.append("({})".format(value.build(ctx)))
            else:
                values.append(value.build(ctx))
        return " {} ".format(self.op).join(values)


class BinOp(CodeExpression):
    def __init__(self, left, op, right):
        super(BinOp, self).__init__()
        self.left = left
        self.op = op
        self.right = right

    def build(self, ctx):
        return " ".join([self.left.build(ctx), self.op, self.right.build(ctx)])


class UnaryOp(CodeExpression):
    def __init__(self, op, operand):
        self.op = op
        self.operand = operand

    def build(self, ctx):
        operand = self.operand.build(ctx)
        if isinstance(self.operand, BoolOp):
            operand = "({})".format(operand)
        return "{}{}".format(self.op, operand)


class Lambda(CodeExpression):
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def build(self, ctx):
        args = self.args.build(ctx)
        body = self.body.build(ctx)
        return "[&]({}) -> auto {{ return {}; }}".format(args, body)


class IfExp(CodeExpression):
    def __init__(self, test, body, orelse):
        self.test = test
        self.body = body
        self.orelse = orelse

    def build(self, ctx):
        test = self.test.build(ctx)
        body = self.body.build(ctx)
        orelse = self.orelse.build(ctx)
        return "(({}) ? ({}) : ({}))".format(test, body, orelse)


class Call(CodeExpression):
    def __init__(self, func, args=[], keywords=[], starargs=None, kwargs=None):
        self.func = func
        self.args = args
        self.keywords = keywords
        self.starargs = starargs
        self.kwargs = kwargs

    def build(self, ctx):
        args = ", ".join([x.build(ctx) for x in self.args])
        return "{}({})".format(self.func.build(ctx), args)


class Num(CodeExpression):
    def __init__(self, n):
        super(Num, self).__init__()
        self.n = n

    def build(self, ctx):
        return "{}".format(self.n)


class Attribute(CodeExpression):
    def __init__(self, value, attr):
        super(Attribute, self).__init__()
        self.value = value
        self.attr = attr

    def build(self, ctx):
        return "{}.{}".format(self.value.build(ctx), self.attr)


class Name(CodeExpression):
    def __init__(self, id):
        super(Name, self).__init__()
        self.id = id

    def build(self, ctx):
        # boolean special case
        if self.id == "True":
            return "true"
        elif self.id == "False":
            return "false"
        return self.id


class arguments(Base):
    def __init__(self, args, vararg, kwarg, defaults):
        self.args = args
        self.vararg = vararg
        self.kwarg = kwarg
        self.defaults = defaults
        self.types = {}

    def get_arg_names(self, ctx):
        return [x.build(ctx) for x in self.args]

    def get_arg_values(self, ctx):
        return [x.build(ctx) for x in self.defaults]

    def set_arg_type(self, name, type):
        #assert name in self.get_arg_names(ctx)
        self.types[name] = type

    def build(self, ctx):
        types = dict(self.types)
        names = self.get_arg_names(ctx)
        values = self.get_arg_values(ctx)
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


class keyword(Base):
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def build(self, ctx):
        return "static const auto {} = {}".format(
            self.name,
            self.value.build(ctx)
        )


#
# for C++ syntax special case
#

class CppScope(Attribute):
    def build(self, ctx):
        return "{}::{}".format(self.value.build(ctx), self.attr)
