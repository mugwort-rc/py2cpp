# -*- coding: utf-8 -*-

import ast

class Converter(ast.NodeVisitor):
    def __init__(self):
        self.items = []

    def add_code(self, code):
        self.items.append(code)

    def visit_Expr(self, node):
        self.generic_visit(node)
        self.add_code(";")

    def visit_BinOp(self, node):
        if node.op.__class__ == ast.Pow:
            self.add_code("std::pow(")
            self.visit(node.left)
            self.add_code(", ")
            self.visit(node.right)
            self.add_code(")")
            return
        elif node.op.__class__ == ast.FloorDiv:
            self.add_code("int(")
            self.visit(node.left)
            self.visit(ast.Div())
            self.visit(node.right)
            self.add_code(")")
            return
        self.visit(node.left)
        self.visit(node.op)
        self.visit(node.right)

    def visit_Add(self, node):
        self.add_code("+")
    def visit_Sub(self, node):
        self.add_code("-")
    def visit_Mult(self, node):
        self.add_code("*")
    def visit_Div(self, node):
        self.add_code("/")
    def visit_Mod(self, node):
        self.add_code("%")
    def visit_LShift(self, node):
        self.add_code("<<")
    def visit_RShift(self, node):
        self.add_code(">>")
    def visit_BitOr(self, node):
        self.add_code("|")
    def visit_BitXor(self, node):
        self.add_code("^")
    def visit_BitAnd(self, node):
        self.add_code("&")

    def visit_Name(self, node):
        self.add_code(node.id)
        # TODO: node.ctx

    def visit_Num(self, node):
        self.add_code("{}".format(node.n))
