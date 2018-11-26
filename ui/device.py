#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os,  time
import ConfigParser
from PySide.QtCore import QThread, Signal
import sys
import yaml
sys.path.append('..')
from framework import device
from common.common import Log, defaultConf

monkeyConfFile = defaultConf

class Device():
    """get or delete device"""
    def __init__(self, app_type):
        self.deviceList = []
        self.deviceStatus = 0
        self.app_type = app_type
        self.deviceObj = device.Device()

    def get_device(self):
        with open(monkeyConfFile, "r") as f:
            for line in f.readlines():
                if "device" in line:
                    return line.split(" = ")[1]
        return []

    def get_android_devices(self):
        devices_list = []
        devices = os.popen('adb devices')
        time.sleep(3)
        devices = devices.read()
        device_split = devices.split('\n')
        for device in device_split:
            if '\tdevice' in device:
                device = device.replace('\tdevice', '')
                devices_list.append(device)
        # p = re.compile('\n([\s\S]+?)\s*device\n')
        # devices_list = re.findall('([\s\S]+)\tdevice\n', devices)
        return devices_list

    def del_device(self):
        """
        delete all devices
        :return:
        """
        with open(monkeyConfFile, "r") as f:
            lines = f.readlines()
        with open(monkeyConfFile, "w") as f_w:
            for line in lines:
                if "deviceList" in line:
                    f_w.write("deviceList = [] \n")
                    continue
                f_w.write(line)

    def device_status(self,device):
        """
        set device status. 0：reachable, 1:unreachable, 2:busy
        :return:
        """
        try:
            status = self.deviceObj.device_status(self.app_type, device)
            print status
            if status == 2:
                return "Running"
            if status == 0:
                return "Connected"
            if status == 1:
                return "Unreachable"
        except:
            pass


class ThreadDeviceStatus(QThread):
    trigger = Signal(str)   # trigger传输的内容是字符串

    def __init__(self, app_type=None, parent=None):
        super(ThreadDeviceStatus, self).__init__(parent)
        self.status = ""
        self.device = ""
        self.app_type = app_type
        self.deviceObj = device.Device()

    def setup(self):
        pass

    def run(self):  # 很多时候都必重写run方法, 线程start后自动运行
        while 1:
            cf = ConfigParser.ConfigParser()
            cf.read(monkeyConfFile)
            deviceList = yaml.load(cf.get('Monkey', 'deviceList'))
            for device in deviceList:
                status = self.deviceObj.device_status(self.app_type, device)
                print status
                if status == 2:
                    self.trigger.emit("Running")
                    Log.warning("device:%s is Running" % device)
                if status == 0:
                    self.trigger.emit("Connected")
                    Log.info("device:%s is Connected" % device)
                if status == 1:
                    self.trigger.emit("Unreachable")
                    Log.error("device:%s is Unreachable" % device)
            time.sleep(10)

if __name__ == '__main__':
    deviceObj = Device()
    print deviceObj.device_status("192.168.64.120")