# -*- coding: utf-8 -*-

import ast

from ..converter import Converter

def convert(src):
    node = ast.parse(src)
    conv = Converter()
    return conv.visit(node)


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
