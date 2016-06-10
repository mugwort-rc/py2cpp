# -*- coding: utf-8 -*-

import ast

import six

from PyQt4.Qt import *

from ui.mainwindow import Ui_MainWindow

from models import ASTTreeModel


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.treeModel = ASTTreeModel(self)
        self.ui.treeView.setModel(self.treeModel)

    @pyqtSlot()
    def on_actionParse_triggered(self):
        source = six.text_type(self.ui.plainTextEdit.toPlainText())
        node = ast.parse(source)
        self.treeModel.setNode(node)
        self.ui.treeView.expandAll()
