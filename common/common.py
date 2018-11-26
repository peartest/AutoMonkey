#!/usr/bin/env python
# -*- coding:utf-8 -*-

import time
import os
from logging_manager import Logger
from PySide import QtGui

exitFlag = False
logFile = os.path.join(os.getcwd(), "Result", "AutoMonkey.log")
if not os.path.exists(os.path.join(os.getcwd(), "Result")):
    os.mkdir(os.path.join(os.getcwd(), "Result"))
Log = Logger(logFile)
defaultConf = os.path.join(os.getcwd(), "conf", "default.conf")
monkeyLogClose = False


def timeOut(dline, process):
    while time.time() < dline and process.poll() == None:
        pass
    if process.poll() == None:
        process.terminate()
        return True
    return False


def showDialog(title, message):
    QtGui.QMessageBox.information(None, title, message)


def saveConfDialog(obj):
    text, ok = QtGui.QInputDialog.getText(obj, 'Input Dialog',
                                          'Save parameter settings followed to other file, Please Enter New File name:')
    if ok:
        return text
    return 0


def importConfDialog(obj):
    filename = QtGui.QFileDialog.getOpenFileName(obj, 'Open file', './conf')
    try:
        with open(filename[0], 'r') as f:
            return f.read()
    except Exception as e:
        return ""



