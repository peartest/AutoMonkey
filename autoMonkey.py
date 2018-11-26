#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PySide import QtGui, QtCore
from PySide.QtGui import *
from ui import androidWindow
from ui import linuxWindow
from common import static

class MainUI(QWidget):

    def __init__(self):
        super(MainUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(250,200)
        self.QBox= QComboBox(self)
        self.QBox.addItem(QIcon(static.androidDevice),  'Android')
        self.QBox.addItem(QIcon(static.findDevice), 'Linux')
        self.QBox.setGeometry(QtCore.QRect(70, 100, 120, 23))
        self.startButton = QPushButton('Start', self)
        self.startButton.setGeometry(QtCore.QRect(80, 150, 95, 23))
        self.startButton.clicked.connect(self.get_boxtext)
        self.setWindowTitle(static.title)
        self.show()

    def get_boxtext(self):
        app.closeAllWindows()
        a = self.QBox.currentText()
        print a
        if a == 'Android':
            Android_window = androidWindow.MainWindow()
            Android_window.show()
            Android_window.exec_()
        else:
            Android_window = linuxWindow.MainWindow()
            Android_window.show()
            Android_window.exec_()

def main():
    global app
    app = QtGui.QApplication(sys.argv)
    ex = MainUI()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()