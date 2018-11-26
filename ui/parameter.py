#!/usr/bin/env python
# -*- coding:utf-8 -*-

import ConfigParser
from common.common import Log, defaultConf

monkeyConfFile = defaultConf

class Parameter():

    def __init__(self):
        """
        init event type and it's value
        """
        pass

    def _get_eventType(self):
        try:
            cf = ConfigParser.ConfigParser()
            cf.read(monkeyConfFile)
            throttle = cf.get('Monkey', '--throttle')
            return "--throttle " + throttle
        except AttributeError, e:
            pass

        return ""

    def _get_eventPercent(self):
        eventString = ""
        with open(monkeyConfFile, 'r') as f:
            for line in f.readlines():
                Log.info(line)
                if "--pct-touch" in line:
                    eventString = eventString + "--pct-touch " + line.split(" = ")[1].split("\n")[0] + " "
                if "--pct-motion" in line:
                    eventString = eventString + "--pct-motion " + line.split(" = ")[1].split("\n")[0] + " "

        return eventString

    def _get_times(self):
        cf = ConfigParser.ConfigParser()
        cf.read(monkeyConfFile)
        times = cf.get('Monkey', 'times')
        return times

    def set_commandString(self, flag):
        if flag == 0:
            commandString = "cd /tmp && ./qmonkey -a HMI -v-v "
            commandString = commandString + self._get_eventPercent() + self._get_eventType() + " " + self._get_times()
        else:
            commandString = self._get_eventType() + ';' + self._get_times()
        return commandString
