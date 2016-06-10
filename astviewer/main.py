#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from PyQt4.QtGui import QApplication

from mainwindow import MainWindow


def main(args):
    app = QApplication(args)

    win = MainWindow()
    win.show()

    return app.exec_()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
