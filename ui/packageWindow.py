# -*- coding:utf-8 -*-
import os
import re
from PySide.QtCore import *
from PySide.QtGui import *
import device

class MainWindow(QDialog):
    """package settings UI"""
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()
        self.setWindowTitle('Packages')

    def get_packages(self):
        deviceobj = device.Device('Android')
        deviceList = deviceobj.get_android_devices()
        app_list = []
        if len(deviceList) > 0:
            app_content = os.popen('adb -s %s shell monkey -v -v 5' % deviceList[0])
            app_read = app_content.read()
            app_split = app_read.split('\n')
            for app in app_split:
                if app != '':
                    if 'from package' in app:
                        app = app.split('from package')[-1].replace(')', '')
                        app_list.append(app)
        return app_list

    def get_pack_button(self):
        pass

