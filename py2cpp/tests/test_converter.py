# -*- coding: utf-8 -*-

import ast

from ..converter import Converter

def convert(src):
    node = ast.parse(src)
    conv = Converter()
    return conv.visit(node)


class TestBoolOp:
    def test_And(self):
        conv = convert("a and b")
        assert [x.build() for x in conv] == ["a && b;"]

    def test_Or(self):
        conv = convert("a or b")
        assert [x.build() for x in conv] == ["a || b;"]

    def test_AndOr(self):
        conv = convert("a and b or c and d")
        assert [x.build() for x in conv] == ["(a && b) || (c && d);"]

    def test_AndOr2(self):
        conv = convert("a and (b or c) and d")
        assert [x.build() for x in conv] == ["a && (b || c) && d;"]


class TestBinOp:
    def test_Add(self):
        conv = convert("x + 1")
        assert [x.build() for x in conv] == ["x + 1;"]

    def test_Sub(self):
        conv = convert("x - 1")
        assert [x.build() for x in conv] == ["x - 1;"]

    def test_Mult(self):
        conv = convert("x * 1")
        assert [x.build() for x in conv] == ["x * 1;"]

    def test_Div(self):
        conv = convert("x / 1")
        assert [x.build() for x in conv] == ["x / 1;"]

    def test_Mod(self):
        conv = convert("x % 1")
        assert [x.build() for x in conv] == ["x % 1;"]

    def test_LShift(self):
        conv = convert("x << 1")
        assert [x.build() for x in conv] == ["x << 1;"]

    def test_RShift(self):
        conv = convert("x >> 1")
        assert [x.build() for x in conv] == ["x >> 1;"]

    def test_BitOr(self):
        conv = convert("x | 1")
        assert [x.build() for x in conv] == ["x | 1;"]

    def test_BitXor(self):
        conv = convert("x ^ 1")
        assert [x.build() for x in conv] == ["x ^ 1;"]

    def test_BitAnd(self):
        conv = convert("x & 1")
        assert [x.build() for x in conv] == ["x & 1;"]

    def test_Pow(self):
        conv = convert("x ** 1")
        assert [x.build() for x in conv] == ["std::pow(x, 1);"]

    def test_FloorDiv(self):
        conv = convert("x // 1")
        assert [x.build() for x in conv] == ["int(x / 1);"]


class TestUnaryOp:
    def test_Invert(self):
        conv = convert("~a")
        assert [x.build() for x in conv] == ["~a;"]

    def test_Not(self):
        conv = convert("not a")
        assert [x.build() for x in conv] == ["!a;"]

    def test_Not_with_BoolOp(self):
        conv = convert("not a and b")
        assert [x.build() for x in conv] == ["!a && b;"]

    def test_Not_with_BoolOp2(self):
        conv = convert("not (a and b)")
        assert [x.build() for x in conv] == ["!(a && b);"]

    def test_UAdd(self):
        conv = convert("+a")
        assert [x.build() for x in conv] == ["+a;"]

    def test_USub(self):
        conv = convert("-a")
        assert [x.build() for x in conv] == ["-a;"]


class TestLambda:
    def test_Lambda(self):
        conv = convert("lambda x: x + 1")
        assert [x.build() for x in conv] == ["[&](int x) -> auto { return x + 1; };"]

    def test_Lambda_set_arg_type(self):
        node = ast.parse("lambda x: x + 1")
        conv = Converter()
        ret = conv.visit(node)
        conv.arguments[0].set_arg_type("x", "double")
        assert [x.build() for x in ret] == ["[&](double x) -> auto { return x + 1; };"]


class TestIfExp:
    def test_IfExp(self):
        conv = convert("a if True else b")
        assert [x.build() for x in conv] == ["((True) ? (a) : (b));"]
