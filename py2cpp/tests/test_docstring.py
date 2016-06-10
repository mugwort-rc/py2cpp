# -*- coding: utf-8 -*-

from ..docstring import get_params
from ..docstring import get_rtype
from ..docstring import parse_type_of


class TestGetParams:
    def test_get_params0(self):
        params = get_params("""
:rtype: int
""")
        assert params == []

    def test_get_params1(self):
        params = get_params("""
:param type name: doc
""")
        assert params == [
            {
                "type": "type",
                "param": "name",
                "doc": "doc",
            },
        ]

    def test_get_params2(self):
        params = get_params("""
:param type name1: doc1
:param type name2: doc2
""")
        assert params == [
            {
                "type": "type",
                "param": "name1",
                "doc": "doc1",
            },
            {
                "type": "type",
                "param": "name2",
                "doc": "doc2",
            },
        ]


class TestGetRType:
    def test_get_rtype0(self):
        rtype = get_rtype("""
:param type name: doc
""")
        assert rtype is None

    def test_get_rtype1(self):
        rtype = get_rtype("""
:rtype: int
""")
        assert rtype == "int"

    def test_get_rtype2(self):
        rtype = get_rtype("""
:rtype: int
:rtype: float
""")
        assert rtype == "int"

    def test_get_rtype_of(self):
        rtype = get_rtype("""
:rtype: list of str
""")
        assert rtype == "list of str"


class TestParseTypeOf:
    def test_parse_type_of1(self):
        types = parse_type_of("list")
        assert types == "list"

    def test_parse_type_of2(self):
        types = parse_type_of("list of str")
        assert types == ("list", "str")

    def test_parse_type_of3(self):
        types = parse_type_of("list of map of (str, str)")
        assert types == ("list", ("map", "(str, str)"))
