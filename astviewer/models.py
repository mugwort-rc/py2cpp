# -*- coding: utf-8 -*-

import types

from PyQt4.QtCore import QAbstractItemModel
from PyQt4.QtCore import QModelIndex
from PyQt4.QtCore import QVariant
from PyQt4.QtCore import Qt


class ASTTreeModel(QAbstractItemModel):
    def __init__(self, parent):
        super(ASTTreeModel, self).__init__(parent)
        self.headers = [
            self.tr("Attribute"),
            self.tr("Value"),
        ]
        self.node = None

    def setNode(self, node):
        self.beginResetModel()
        # create root item (unvisible)
        self.node = ASTTreeItem(None, None)
        self.node.children.append(ASTTreeItem.create(node, self.node))
        self.endResetModel()

    def columnCount(self, parent=QModelIndex()):
        return 2

    def rowCount(self, parent=QModelIndex()):
        if self.node is None:
            return 0
        parent_item = None
        if not parent.isValid():
            parent_item = self.node
        else:
            parent_item = parent.internalPointer()
        return len(parent_item.children)

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()
        node = index.internalPointer()
        if index.column() == 0:
            return node.name
        elif index.column() == 1:
            return node.value
        return QVariant()

    def index(self, row, column, parent=QModelIndex()):
        parent_item = None
        if not parent.isValid():
            parent_item = self.node
        else:
            parent_item = parent.internalPointer()
        return self.createIndex(row, column, parent_item.children[row])

    def parent(self, index):
        item = index.internalPointer()
        if item.parent is None:
            # root case
            return QModelIndex()
        return self.createIndex(item.parent.row, 0, item.parent)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Vertical or role != Qt.DisplayRole:
            return QVariant()
        elif orientation == Qt.Horizontal:
            return self.headers[section]


class ASTTreeItem(object):

    NODE_TYPE = 1
    FIELD_TYPE = 2

    def __init__(self, type, node, parent=None):
        self.type = type
        self.node = node
        self.parent = parent
        self.children = []

    @property
    def name(self):
        return "<{}>".format(self.node.__class__.__name__)

    @property
    def row(self):
        if self.parent is None:
            # root case
            return 0
        return self.parent.children.index(self)

    @property
    def value(self):
        return ""

    @staticmethod
    def create(node, parent=None):
        item = ASTTreeItem(ASTTreeItem.NODE_TYPE, node, parent=parent)
        for field in node._fields:
            obj = getattr(node, field)
            item.children.append(ASTAttrTreeItem.create(field, obj, item))
        return item

        
class ASTAttrTreeItem(ASTTreeItem):
    def __init__(self, field, node, parent=None):
        super(ASTAttrTreeItem, self).__init__(ASTTreeItem.FIELD_TYPE, node, parent)
        self.field = field

    @property
    def name(self):
        return "@" + self.field

    @property
    def value(self):
        if len(self.children) == 0:
            return self.node
        return ""

    @staticmethod
    def create(field, node, parent=None):
        item = ASTAttrTreeItem(field, node, parent)
        if isinstance(node, list):
            for child in node:
                item.children.append(ASTTreeItem.create(child, parent=item))
        elif not isinstance(node, (str, int, float, types.NoneType)):
            item.children.append(ASTTreeItem.create(node, parent=item))
        return item
