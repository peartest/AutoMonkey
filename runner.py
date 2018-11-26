#!/usr/bin/env python
# -*- coding:utf-8 -*-

import subprocess
import sys, os
import time, datetime

from common import static, common
from ui import parameter
import setupMonkey
from framework import run
from common.common import Log
from PySide.QtCore import QThread, Signal
from AutoBot import LinuxTestLibrary

timeout = 5


class ThreadRun(QThread):
    trigger = Signal()   # trigger传输的内容是字符串

    def __init__(self, parent=None):
        super(ThreadRun, self).__init__(parent)

    def setup(self):
        pass

    def run(self):
        self.trigger.emit()


class Runner():

    def __init__(self, logFilePath, flag):
        parameterObj = parameter.Parameter()
        self.commandString = parameterObj.set_commandString(flag)
        self.logFilePath = logFilePath
        self.startTime = 0
        self.flag = flag

    def start(self, deviceList):
        if self.flag == 0:
            pushFile = setupMonkey.Setup()
            pushFile.push(deviceList[0])
            if self.commandString != None:
                Log.info("command:%s" % self.commandString)
                self.runner = run.Runner(deviceList, self.commandString, self.logFilePath)
                self.runner.run()
                Log.info("running monkey")
        else:
            self.runner = run.AndroidRunner(deviceList, self.commandString, self.logFilePath)
            self.runner.run()
            Log.info("running monkey")

    def stop_android(self):
        self.runner.stop()

    def stop(self, device, end=False):
        autobot_lib = LinuxTestLibrary()
        autobot_lib.connect_to_device_ssh(device)
        autobot_lib.exec_ssh_cmd("killall -9 tail && killall -9 qmonkey")
        autobot_lib.cur_connector.close_shell()  # 最好先close
        autobot_lib.disconnect_device_ssh()

    def create_report(self, exit=False):
        if exit:
            self.runner.create_report()


if __name__ == '__main__':
    deviceList = [sys.argv[1]]
    print sys.argv[2:]
    test = Runner()
    test.start(deviceList)
