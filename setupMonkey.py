#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
from AutoBot import LinuxTestLibrary

DIR = os.getcwd()
qmonkeyTool = os.path.join(DIR,  'tools', 'qmonkey')
deviceConf = os.path.join(DIR,  'tools', 'device.conf')
libinjectevent = os.path.join(DIR,  'tools', 'libinjectevent.so')
libinjectevent0 = os.path.join(DIR,  'tools', 'libinjectevent.so.0')
libinjectevent1 = os.path.join(DIR,  'tools', 'libinjectevent.so.0.1')
fileList = [deviceConf, qmonkeyTool]
libfile = [libinjectevent, libinjectevent0, libinjectevent1]

class Setup():
    def __init__(self):
        pass

    def push(self, device):
        autobot_lib = LinuxTestLibrary()
        autobot_lib.connect_to_device_ssh(device)
        for file in fileList:
            print file
            autobot_lib.scp_push_file(file, '/tmp/', device)
        for lib in libfile:
            autobot_lib.scp_push_file(lib, '/usr/lib/', device)
        autobot_lib.exec_ssh_cmd("chmod +x /tmp/qmonkey")
        autobot_lib.cur_connector.close_shell()  # 最好先close
        autobot_lib.disconnect_device_ssh()


if __name__ == '__main__':
    p = Setup()
    p.push("192.168.64.156")