#!/usr/bin/env python
# -*- coding:utf-8 -*-

from PySide.QtCore import QThread, Signal
from PySide.QtGui import QApplication
import logging
import subprocess
import os
import time

from common import common

class ConsoleWindowLogHandler(logging.Handler):
    def __init__(self, textBox):
        super(ConsoleWindowLogHandler, self).__init__()
        self.textBox = textBox

    def emit(self, logRecord):
        self.textBox.append(str(logRecord.getMessage()))

class ThreadLogShow(QThread):
    trigger = Signal(str)

    def __init__(self, parent=None):
        super(ThreadLogShow, self).__init__(parent)

    def setup(self, filename):
        self.filename = filename

    def run(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as t:
                t.seek(0, 2)
                while True:
                    if common.exitFlag:
                        break
                    if "AutoMonkey.log" not in self.filename and "Monkey.log" in self.filename and common.monkeyLogClose:
                        break
                    line = t.readline().strip()
                    if not line:
                        continue
                    self.trigger.emit(line)
                    time.sleep(0.3)

            # with open(self.filename, 'a+') as f:
            #     self.trigger.emit(f.read())
            # command = pythonPath + " " + mytailPath + " " + self.filename
            # process = subprocess.Popen(command, shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            # while process.poll() is None:
            #     if common.exitFlag:
            #         break
            #     line = process.stdout.readline().strip()
            #     if line != "":
            #         self.trigger.emit(line)


#
class LogShow(logging.Logger):
    def __init__(self, textBox):
        logging.Logger.__init__(self, "", level="DEBUG")
        consoleHandler = ConsoleWindowLogHandler(textBox)
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        consoleHandler.setFormatter(formatter)
        self.addHandler(consoleHandler)


if __name__ == '__main__':
    pass