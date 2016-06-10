# -*- coding: utf-8 -*-


class TypeRegistry(object):
    def __init__(self):
        self.type_map = {}

    def __contains__(self, v):
        return v in self.type_map

    def convert(self, type_str):
        raise NotImplementedError

    def register(self, pytype, cpptype):
        self.type_map[pytype] = cpptype
