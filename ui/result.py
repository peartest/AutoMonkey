#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PySide.QtCore import QThread, Signal
import os

from common import common

class ThreadGetResult(QThread):
    trigger = Signal(bool)   # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(ThreadGetResult, self).__init__(parent)
        self.filename = ""

    def setup(self, filename):
        self.filename = filename

    def run(self):
        if self.filename != "":
            os.system(self.filename)  # self.trigger.emit(line)




