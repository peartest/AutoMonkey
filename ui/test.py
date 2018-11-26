#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from PySide import QtGui, QtCore
from PySide.QtGui import *
import linuxWindow
import androidWindow
from common import static

class MainUI(QWidget):

    def __init__(self):
        super(MainUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.QBox= QComboBox(self)
        self.QBox.addItem(QIcon(static.storePNG),  'Android')
        self.QBox.addItem(QIcon(static.storePNG), 'Linux')
        self.QBox.setGeometry(QtCore.QRect(40, 30, 75, 23))
        self.startButton = QPushButton('Start', self)
        self.startButton.setGeometry(QtCore.QRect(40, 60, 75, 23))
        self.startButton.clicked.connect(self.get_boxtext)
        self.setWindowTitle('AutoMonkey')
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