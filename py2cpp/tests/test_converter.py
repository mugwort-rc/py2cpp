# -*- coding: utf-8 -*-

import ast

from ..converter import Converter
from ..cpp import BuildContext

def convert(src):
    node = ast.parse(src)
    conv = Converter()
    return conv.visit(node)


def build(node):
    ctx = BuildContext.create()
    return [x.build(ctx) for x in node]


class TestFunctionDef:
    def test_pass(self):
        conv = convert("""
def test():
    pass
""".strip())
        assert build(conv) == ["void test() {\n\n}"]

    def test_BoolOp(self):
        conv = convert("""
def test():
    a and b
""".strip())
        assert build(conv) == ["void test() {\n    a && b;\n}"]

    def test_BinOp(self):
        conv = convert("""
def test():
    a + b
""".strip())
        assert build(conv) == ["void test() {\n    a + b;\n}"]

    def test_UnaryOp(self):
        conv = convert("""
def test():
    ~a
""".strip())
        assert build(conv) == ["void test() {\n    ~a;\n}"]

    def test_Lambda(self):
        conv = convert("""
def test():
    lambda x: x + 1
""".strip())
        assert build(conv) == ["void test() {\n    [&](int x) -> auto { return x + 1; };\n}"]

    def test_IfExp(self):
        conv = convert("""
def test():
    a if x else b
""".strip())
        assert build(conv) == ["void test() {\n    ((x) ? (a) : (b));\n}"]

    def test_docstring(self):
        conv = convert("""
def test():
    "docstring"
    pass
""".strip())
        assert conv[0].docstring == "docstring"


class TestClassDef:
    def test_pass(self):
        conv = convert("""
class test:
    pass
""".strip())
        assert build(conv) == ["class test {\n\n};"]

    def test_self(self):
        conv = convert("""
class test(a, b):
    def test(self):
        pass
""".strip())
        assert build(conv) == ["class test : public a, public b {\n    void test() {\n\n    }\n};"]

    def test_docstring(self):
        conv = convert("""
class test:
    "docstring"
    pass
""".strip())
        assert conv[0].docstring == "docstring"


class TestReturn:
    def test_return(self):
        conv = convert("return")
        assert build(conv) == ["return;"]

    def test_return_with_value(self):
        conv = convert("return 1")
        assert build(conv) == ["return 1;"]


class TestAssign:
    def test_assign(self):
        conv = convert("a = 1")
        assert build(conv) == ["a = 1;"]

    def test_assigns(self):
        conv = convert("a = b = c")
        assert build(conv) == ["a = b = c;"]


class TestAugAssign:
    def test_Add(self):
        conv = convert("x += 1")
        assert build(conv) == ["x += 1;"]

    def test_Sub(self):
        conv = convert("x -= 1")
        assert build(conv) == ["x -= 1;"]

    def test_Mult(self):
        conv = convert("x *= 1")
        assert build(conv) == ["x *= 1;"]

    def test_Div(self):
        conv = convert("x /= 1")
        assert build(conv) == ["x /= 1;"]

    def test_Mod(self):
        conv = convert("x %= 1")
        assert build(conv) == ["x %= 1;"]

    def test_LShift(self):
        conv = convert("x <<= 1")
        assert build(conv) == ["x <<= 1;"]

    def test_RShift(self):
        conv = convert("x >>= 1")
        assert build(conv) == ["x >>= 1;"]

    def test_BitOr(self):
        conv = convert("x |= 1")
        assert build(conv) == ["x |= 1;"]

    def test_BitXor(self):
        conv = convert("x ^= 1")
        assert build(conv) == ["x ^= 1;"]

    def test_BitAnd(self):
        conv = convert("x &= 1")
        assert build(conv) == ["x &= 1;"]

    def test_Pow(self):
        conv = convert("x **= 1")
        assert build(conv) == ["x = std::pow(x, 1);"]

    def test_FloorDiv(self):
        conv = convert("x //= 1")
        assert build(conv) == ["x = int(x / 1);"]


class TestFor:
    def test_for(self):
        conv = convert("""
for i in x:
    pass
""".strip())
        assert build(conv) == ["for (auto i : x) {\n\n}"]


class TestWhile:
    def test_while1(self):
        conv = convert("""
while True:
    break
""".strip())
        assert build(conv) == ["while (true) {\n    break;\n}"]

    def test_while2(self):
        conv = convert("""
while True or False:
    continue
""".strip())
        assert build(conv) == ["while (true || false) {\n    continue;\n}"]


class TestIf:
    def test_if(self):
        conv = convert("""
if True:
    pass
""".strip())
        assert build(conv) == ["if (true) {\n\n}"]

    def test_if_orelse1(self):
        conv = convert("""
if True:
    pass
else:
    pass
""".strip())
        assert build(conv) == ["if (true) {\n\n} else {\n\n}"]

    def test_if_orelse2(self):
        conv = convert("""
if a:
    pass
elif b:
    pass
else:
    pass
""".strip())
        assert build(conv) == ["if (a) {\n\n} else if (b) {\n\n} else {\n\n}"]


class TestRaise:
    def test_type(self):
        conv = convert("raise NotImplementedError")
        assert build(conv) == ["throw NotImplementedError();"]


class TestBoolOp:
    def test_And(self):
        conv = convert("a and b")
        assert build(conv) == ["a && b;"]

    def test_Or(self):
        conv = convert("a or b")
        assert build(conv) == ["a || b;"]

    def test_AndOr(self):
        conv = convert("a and b or c and d")
        assert build(conv) == ["(a && b) || (c && d);"]

    def test_AndOr2(self):
        conv = convert("a and (b or c) and d")
        assert build(conv) == ["a && (b || c) && d;"]


class TestBinOp:
    def test_Add(self):
        conv = convert("x + 1")
        assert build(conv) == ["x + 1;"]

    def test_Sub(self):
        conv = convert("x - 1")
        assert build(conv) == ["x - 1;"]

    def test_Mult(self):
        conv = convert("x * 1")
        assert build(conv) == ["x * 1;"]

    def test_Div(self):
        conv = convert("x / 1")
        assert build(conv) == ["x / 1;"]

    def test_Mod(self):
        conv = convert("x % 1")
        assert build(conv) == ["x % 1;"]

    def test_LShift(self):
        conv = convert("x << 1")
        assert build(conv) == ["x << 1;"]

    def test_RShift(self):
        conv = convert("x >> 1")
        assert build(conv) == ["x >> 1;"]

    def test_BitOr(self):
        conv = convert("x | 1")
        assert build(conv) == ["x | 1;"]

    def test_BitXor(self):
        conv = convert("x ^ 1")
        assert build(conv) == ["x ^ 1;"]

    def test_BitAnd(self):
        conv = convert("x & 1")
        assert build(conv) == ["x & 1;"]

    def test_Pow(self):
        conv = convert("x ** 1")
        assert build(conv) == ["std::pow(x, 1);"]

    def test_FloorDiv(self):
        conv = convert("x // 1")
        assert build(conv) == ["int(x / 1);"]


class TestUnaryOp:
    def test_Invert(self):
        conv = convert("~a")
        assert build(conv) == ["~a;"]

    def test_Not(self):
        conv = convert("not a")
        assert build(conv) == ["!a;"]

    def test_Not_with_BoolOp(self):
        conv = convert("not a and b")
        assert build(conv) == ["!a && b;"]

    def test_Not_with_BoolOp2(self):
        conv = convert("not (a and b)")
        assert build(conv) == ["!(a && b);"]

    def test_UAdd(self):
        conv = convert("+a")
        assert build(conv) == ["+a;"]

    def test_USub(self):
        conv = convert("-a")
        assert build(conv) == ["-a;"]


class TestLambda:
    def test_Lambda(self):
        conv = convert("lambda x: x + 1")
        assert build(conv) == ["[&](int x) -> auto { return x + 1; };"]

    def test_Lambda_set_arg_type(self):
        node = ast.parse("lambda x: x + 1")
        conv = Converter()
        ret = conv.visit(node)
        conv.arguments[0].set_arg_type("x", "double")
        ctx = BuildContext.create()
        assert [x.build(ctx) for x in ret] == ["[&](double x) -> auto { return x + 1; };"]


class TestIfExp:
    def test_IfExp(self):
        conv = convert("a if True else b")
        assert build(conv) == ["((true) ? (a) : (b));"]


class TestStr:
    def test_str(self):
        conv = convert('"test"')
        assert build(conv) == ['"test";']

    def test_quote(self):
        conv = convert('"te\\"st"')
        assert build(conv) == ['"te\\"st";']
