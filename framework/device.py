# coding:utf8
from AutoBot import LinuxTestLibrary
import os
import re
import time

class LoginError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)
        self.msg = msg

    def __str__(self):
        return "%s" % (self.msg)

class LoginTimeoutError(LoginError):
    def __init__(self):
        LoginError.__init__(self, "Login timeout expired")


class Device():
    def __init__(self):
        pass

    def get_devices(self):
        devices_list = []
        devices = os.popen('adb devices')
        time.sleep(3)
        devices = devices.read()
        device_split = devices.split('\n')
        for device in device_split:
            if '\tdevice' in device:
                device = device.replace('\tdevice', '')
                devices_list.append(device)
        return devices_list

    def device_status(self, app_type, value, type = 'ssh'):
        if app_type == 'android':
            device = os.popen('adb devices')
            device_statu = device.read()
            if '\t' in device_statu:
                monkey = os.popen("adb -s %s shell ps -A" % value)
                if 'monkey' in monkey.read():
                    result = 2
                else:
                    result = 0
            else:
                result = 1
        else:
            lib = LinuxTestLibrary()
            if type == 'ssh':
                try:
                    try:
                        lib.connect_to_device_ssh(value)
                    except:
                        result = 1
                    else:
                        res = lib.exec_ssh_cmd('ps')
                        if 'qmonkey' in res:
                            result = 2
                        else:
                            result = 0
                except LoginError:
                    LoginError('Login Error')
                    result = 1
                finally:
                    try:
                        lib.cur_connector.close_shell()
                        lib.disconnect_device_ssh()
                    except:
                        result = 1
            elif type == 'serial':
                try:
                    try:
                        lib.connect_to_device_serial(value)
                    except:
                        result = 1
                    else:
                        res = lib.exec_serial_cmd('ps')
                        if 'qmonkey' in res:
                            result = 2
                        else:
                            result = 0
                except LoginError:
                    LoginError('Login Error')
                    result = 1
                finally:
                    try:
                        lib.disconnect_device_serial()
                    except:
                        result = 1
            else:
                try:
                    try:
                        lib.connect_to_device_rdb(value)
                    except:
                        result = 1
                    else:
                        res = lib.exec_rdb_shellcmd('ps')
                        if 'qmonkey' in res:
                            result = 2
                        else:
                            result = 0
                except LoginError:
                    LoginError('Login Error')
                    result = 1
                finally:
                    try:
                        lib.disconnect_device_rdb()
                    except:
                        result = 1

        return result

if __name__ == '__main__':
    a = Device()
    a.device_status('192.168.64.156', type= 'ssh')


