#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
import os
import time
import shutil
import yaml
import packageWindow
from PySide.QtCore import *
from PySide.QtGui import *
sys.path.append('..')
from common import static
import runner
import device
from common import common
import result
import datetime
import ConfigParser
DIR = os.getcwd()
monkeyConfFile = common.defaultConf
deviceList = []
app_type = 'android'

class ContentWidget(QDialog):
    def __init__(self, parent=None):
        super(ContentWidget, self).__init__(parent)
        self.hbox = QVBoxLayout(self)
        self.textBrowser = QTextBrowser(self)
        self.hbox.addWidget(self.textBrowser)


class IndexWidget(QDialog):
    def __init__(self, parent=None):
        super(IndexWidget, self).__init__(parent)
        self.hbox = QVBoxLayout(self)
        self.textBrowser = QTextBrowser(self)
        self.hbox.addWidget(self.textBrowser)
        # self.textBrowser.setText("QMonkey")


class ErrorWidget(QDialog):
    def __init__(self, parent=None):
        super(ErrorWidget, self).__init__(parent)
        self.hbox = QVBoxLayout(self)
        self.textBrowser = QTextBrowser(self)
        self.hbox.addWidget(self.textBrowser)
        # self.textBrowser.setText("Error")


class TabWidget(QTabWidget):
    def __init__(self, parent=None):
        super(TabWidget, self).__init__(parent)
        self.resize(400, 300)
        self.mContent = ContentWidget()
        self.mIndex = IndexWidget()
        self.mError = ErrorWidget()
        self.addTab(self.mContent, u"AutoMonkey")
        self.addTab(self.mIndex, u"Monkey")
        self.addTab(self.mError, u"Exception")

class MainWindow(QDialog):
    """monkey_android UI"""
    def __init__(self,parent=None):
        super(MainWindow, self).__init__()
        self.init_conf()
        self.setParent(parent)
        common.Log.info("set up ui")
        self.setup_ui()
        self.findDeviceAction.triggered.connect(self.get_device_status)
        self.deleteDeviceAction.triggered.connect(self.del_device)
        # self.storeButton.clicked.connect(self.set_conf)
        self.startButton.clicked.connect(self.start)
        self.stopButton.clicked.connect(self.stop)
        self.checkLogButton.clicked.connect(self.check)
        self.monkeyButton.clicked.connect(self.checkMonkeyLog)
        self.exportButton.clicked.connect(self.exportConf)
        self.importButton.clicked.connect(self.importConf)
        self.setAbout.triggered.connect(self.about)
        self.startTime = datetime.datetime.now()
        self.secsTime = float(1) * 60 * 60



    def setup_ui(self):
        # main window width hand height
        # self.setMinimumWidth(600)
        self.setMaximumWidth(800)
        self.setMinimumHeight(600)
        # main window title
        self.setWindowTitle(static.title)
        # file menu bar
        self.menuBar = QMenuBar()
        self.menuBar.setMaximumHeight(23)
        # self.menuFile = self.menuBar.addMenu(static.menuFile)
        # self.importAction = QAction(QIcon(static.importPNG), static.importFile, self)
        # self.exportAction = QAction(QIcon(static.exportPNG), static.exportFile, self)
        # self.menuFile.addAction(self.importAction)
        # self.menuFile.addAction(self.exportAction)
        self.setEnvActioin = QAction(QIcon(static.setPNG), static.pcSet, self)
        self.menuSet = self.menuBar.addMenu(static.menuSet)
        self.menuSet.addAction(self.setEnvActioin)

        self.packageSetting = QAction(QIcon(static.setPNG), static.package, self, triggered=self.package_settings)
        self.packageSetting.setStatusTip('Packages')
        self.packageSet = self.menuBar.addMenu(static.package)
        self.packageSet.addAction(self.packageSetting)


        self.setAbout = QAction(QIcon(static.setPNG), static.menuAbout, self)
        self.setAbout.setStatusTip('About')  # 状态栏提示
        self.menuHelp = self.menuBar.addMenu(static.menuHelp)
        self.menuHelp.addAction(self.setAbout)



        # set all layout
        self.hbox = QHBoxLayout(self)

        # device ========
        self.topLeft = QFrame(self)
        self.topLeft.setMaximumSize(218, 300)
        self.topLeft.setMinimumSize(218, 200)
        self.topLeft.setFrameShape(QFrame.StyledPanel)
        self.topLeftLayout = QVBoxLayout(self.topLeft)
        self.toolBar = QToolBar()
        self.findDeviceAction = QAction(QIcon(static.androidDevice), static.findDeviceButton, self)
        self.deleteDeviceAction = QAction(QIcon(static.deleteDevice), static.deleteDeviceButton, self)
        self.toolBar.addAction(self.findDeviceAction)
        self.toolBar.addAction(self.deleteDeviceAction)
        self.deviceLab = QLabel(static.deviceName, self)
        self.device = QTableWidget(1, 2)
        self.device.setHorizontalHeaderLabels(['name', 'status'])
        self.device.setColumnWidth(0, 100)
        self.device.setColumnWidth(1, 80)
        self.topLeftLayout.addWidget(self.deviceLab)
        self.topLeftLayout.addWidget(self.toolBar)

        self.topLeftLayout.addWidget(self.device)


        # set button or other for running monkey or not and status of device and log ========
        self.topRight = QFrame(self)
        self.topRight.setFrameShape(QFrame.StyledPanel)
        self.topRight.setMaximumHeight(40)
        self.startButton = QPushButton(QIcon(static.startPNG), "")
        self.stopButton = QPushButton(QIcon(static.stopPNG), "")

        self.status = QLabel(static.status)
        self.statusEdit = QLineEdit(self)
        self.statusEdit.setReadOnly(True)
        self.statusEdit.setMaximumWidth(80)
        self.statusEdit.setMinimumWidth(80)
        self.statusEdit.setText("")
        # check log
        self.checkLogButton = QPushButton(static.checkLog)
        self.checkLogButton.setMaximumHeight(20)
        self.checkLogButton.setMinimumHeight(20)
        self.checkLogButton.setMaximumWidth(60)
        self.selectLog = QLabel(static.selectlog)
        self.logfile = QComboBox()
        self.dirlist = os.listdir(os.path.join(os.getcwd(), "Result"))
        for d in self.dirlist:
            if d != "AutoMonkey.log":
                self.logfile.insertItem(0, d)
        self.logfile.setMaximumWidth(150)
        self.logfile.setMaximumHeight(20)
        self.logfile.setMinimumHeight(20)
        self.topLayout = QHBoxLayout(self.topRight)
        self.topLayout.addWidget(self.startButton)
        self.topLayout.addWidget(self.stopButton)
        self.topLayout.addWidget(self.status)
        self.topLayout.addWidget(self.statusEdit)
        self.topLayout.addWidget(self.selectLog)
        self.topLayout.addWidget(self.logfile)
        self.topLayout.addWidget(self.checkLogButton)

        # set parameter for monkey =======
        self.midRight = QFrame(self)
        self.midRight.setMaximumSize(555, 200)
        self.midRight.setMinimumSize(555, 200)
        self.midRight.setFrameShape(QFrame.StyledPanel)
        self.midRightLayout = QVBoxLayout(self.midRight)
        self.subLayout0 = QVBoxLayout()
        self.subLayout1 = QVBoxLayout()
        self.subLayout2 = QHBoxLayout()
        self.subLayout3 = QVBoxLayout()
        self.subLayout4 = QVBoxLayout()
        self.subLayout5 = QHBoxLayout()
        self.subLayout6 = QHBoxLayout()
        self.toolBar = QToolBar()
        # self.storeAction = QAction(QIcon(static.storePNG), static.storeButton, self)
        self.startAction = QAction(QIcon(static.startPNG), static.startButton, self)
        self.stopAction = QAction(QIcon(static.stopPNG), static.stopButton, self)
        # self.toolBar.addAction(self.storeAction)
        self.toolBar.addAction(self.startAction)
        self.toolBar.addAction(self.stopAction)
        self.timeLongLbl = QLabel(static.timeString, self)
        self.timeLong = QLineEdit(self)
        self.timeLong.setMaximumWidth(100)
        self.timeLong.setMinimumWidth(100)
        self.timeLong.setPlaceholderText(static.timeLong)
        self.timeLongUnit = QLabel("H")
        self.etSetLbl = QLabel(static.eventTypeSet)
        self.etSet = QTableWidget(2, 2)
        self.etSet.setMaximumHeight(150)
        self.etSet.setHorizontalHeaderLabels(['option', 'value'])
        self.etSet.horizontalHeader().setStretchLastSection(True)
        self.etSet.setItem(0, 0, QTableWidgetItem("--throttle"))
        self.etSet.setItem(1, 0, QTableWidgetItem("package"))
        self.etSet.setItem(0, 1, QTableWidgetItem(str(static.eventType["--throttle"])))
        # set event type percent
        # self.etPercentLbl = QLabel(static.eventTpyePercent, self)
        # self.etPercent = QTableWidget(2, 2)
        # self.etPercent.setMaximumHeight(150)
        # self.etPercent.setHorizontalHeaderLabels(['option', 'value'])
        # self.etPercent.horizontalHeader().setStretchLastSection(True)
        # self.etPercent.setItem(0, 0, QTableWidgetItem("--pct-touch"))
        # self.etPercent.setItem(0, 1, QTableWidgetItem(str(static.eventPercent["--pct-touch"])))
        # self.etPercent.setItem(1, 0, QTableWidgetItem("--pct-motion"))
        # self.etPercent.setItem(1, 1, QTableWidgetItem(str(static.eventPercent["--pct-motion"])))
        # self.storeButton = QPushButton(QIcon(static.storePNG), static.storeButton)
        # self.storeButton.setToolTip(static.storeButton)
        self.exportButton = QPushButton(QIcon(static.exportPNG), static.exportFile)
        self.exportButton.setToolTip(static.exportFile)
        self.importButton = QPushButton(QIcon(static.importPNG), static.importFile)
        self.importButton.setToolTip(static.importFile)
        self.subLayout2.addWidget(self.timeLongLbl)
        self.subLayout2.addWidget(self.timeLong)
        self.subLayout2.addWidget(self.timeLongUnit)
        self.subLayout2.addWidget(QLabel(" " * 300))
        # self.subLayout2.addWidget(self.storeButton)
        self.subLayout2.addWidget(self.exportButton)
        self.subLayout2.addWidget(self.importButton)

        self.subLayout0.addLayout(self.subLayout2)
        self.subLayout3.addWidget(self.etSetLbl)
        self.subLayout3.addWidget(self.etSet)
        # self.subLayout4.addWidget(self.etPercentLbl)
        # self.subLayout4.addWidget(self.etPercent)
        self.subLayout5.addLayout(self.subLayout0)
        self.subLayout6.addLayout(self.subLayout3)
        self.subLayout6.addLayout(self.subLayout4)
        self.midRightLayout.addLayout(self.subLayout5)
        self.midRightLayout.addLayout(self.subLayout6)

        # log ========
        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        # log information
        self.logInfo = QLabel(static.logInfo)
        # information filter
        self.logFilter = QLabel(static.logFilter)
        self.monkeyButton = QPushButton(static.openMonkeyLog)
        self.combo = QComboBox()
        for i in range(len(static.logLevel)):
            self.combo.addItem(static.logLevel[i])
        self.combo.setMaximumWidth(55)
        self.combo.setMaximumHeight(20)
        self.combo.setMinimumHeight(20)
        # information details
        self.bottomLayout = QVBoxLayout(self.bottom)
        self.subLayout = QHBoxLayout()
        self.subLayout.addWidget(self.logInfo)
        for i in range(10):
            self.subLayout.addWidget(QLabel(""))
        self.subLayout.addWidget(self.monkeyButton)
        self.subLayout.addWidget(self.logFilter)
        self.subLayout.addWidget(self.combo)
        self.bottomLayout.addLayout(self.subLayout)
        self.tabwidget = TabWidget()
        self.tabwidget.setMinimumHeight(100)
        self.bottomLayout.addWidget(self.tabwidget)

        # splitter mainWindow ++++++++++++++++++++++++++++++++++++
        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.topRight)
        self.splitter2.addWidget(self.midRight)
        self.splitter0 = QSplitter(Qt.Horizontal)
        self.splitter0.addWidget(self.topLeft)
        self.splitter0.addWidget(self.splitter2)
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.menuBar)
        self.splitter1.addWidget(self.splitter0)
        self.splitter1.addWidget(self.bottom)
        self.hbox.addWidget(self.splitter1)
        self.setLayout(self.hbox)
        self.show()

    def about(self):
        common.showDialog(static.menuAbout, static.dialogAbout)

    def package_settings(self):
        package_Window = packageWindow.MainWindow()
        package_Window.show()
        package_Window.exec_()

    def init_conf(self):
        common.Log.info("init monkey conf")
        with open(monkeyConfFile, "w") as f:
            f.write("[Monkey]" + "\n")
            f.write("deviceList = []" + "\n")
            f.write("times = " + static.times + "\n")
            f.write("--throttle = " + static.eventType["--throttle"] + "\n")
            f.write("package = []" + "\n")

    def setup_env(self):
        pass

    def _set_eventType(self, confFile):
        try:
            option = self.etSet.item(0, 0).text()
            value = self.etSet.item(0, 1).text()
            pack_option = self.etSet.item(1, 0).text()
            pack_value = self.etSet.item(1, 1).text()
            if value > "0":
                with open(confFile, 'a+') as f:
                    f.write(option + " = " + value + "\n")
                    f.write(pack_option + " = " + pack_value + "\n")
        except AttributeError, e:
            pass

    def _set_eventPercent(self, confFile):
        try:
            tmp = 0
            for i in range(2):
                option = self.etPercent.item(i, 0).text()
                value = self.etPercent.item(i, 1).text()
                tmp = tmp + int(value)
                if tmp > 100:
                    common.Log.error("all value should less or equal than 100")
                if value > "0":
                    with open(confFile, 'a+') as f:
                        f.write(option + " = " + value + "\n")
        except AttributeError, e:
            pass

    def _set_times(self, confFile):
        hourTime = self.timeLong.text()
        if hourTime == "" or float(hourTime) <= 0:
            return 1
        else:
            if hourTime:
                self.secsTime = float(hourTime) * 60 * 60
                with open(confFile, 'r') as f:
                    for line in f.readlines():
                        if "throttle" in line:
                            value = line.split(" = ")[1].split("\n")[0]
                delayTime = float(value)
                if delayTime > 0:
                    with open(confFile, 'a+') as f:
                        f.write("times = " + str(int(self.secsTime * 1000 / (delayTime * 2))) + "\n")
            return 0

    def set_conf(self,conFile=monkeyConfFile):
        deviceString = ""
        if os.path.exists(conFile):
            with open(conFile, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if "deviceList" in line:
                        deviceString = line
                        break
            with open(conFile, "w") as f:
                f.write("")

        if deviceString != "":
            with open(conFile, "a+") as f:
                f.write("[Monkey]" + "\n")
                f.write(deviceString)
        # self._set_eventPercent(conFile)
        self._set_eventType(conFile)
        if self._set_times(conFile) == 1:
            common.showDialog("Message", static.dialogSetTime + ", " + static.dialogTimeLong)
            if conFile != monkeyConfFile:
                os.remove(conFile)
            return 1
        else:
            # if conFile == monkeyConfFile:
            #     common.showDialog("Message", static.dialogStorDefaultConf)
            # else:
            #     common.showDialog("Message", static.dialogStoreNewFile)
            return 0

    def _set_device(self):
        """
        get device from ui
        :return: devices list
        """
        global deviceList
        deviceList = []
        try:
            for i in range(2):
                try:
                    device = self.device.item(i, 0).text()
                    deviceList.append(str(device))
                except AttributeError, e:
                    pass
            while "" in deviceList:
                deviceList.remove("")
            if len(deviceList):
                with open(monkeyConfFile, "r") as f:
                    lines = f.readlines()
                with open(monkeyConfFile, "w") as f_w:
                    for line in lines:
                        if "deviceList" in line:
                            f_w.write("deviceList = " + str(deviceList) + "\n")
                            continue
                        f_w.write(line)
            else:
                with open(monkeyConfFile, "r") as f:
                    lines = f.readlines()
                with open(monkeyConfFile, "w") as f_w:
                    for line in lines:
                        if "deviceList" in line:
                            f_w.write("deviceList = [] \n")
                            continue
                        f_w.write(line)
        except AttributeError, e:
            pass


    def get_device_status(self):
        """
        set device status
        """
        cf = ConfigParser.ConfigParser()
        cf.read(monkeyConfFile)
        deviceList = yaml.load(cf.get('Monkey', 'deviceList'))
        if deviceList == []:
            deviceobj = device.Device(app_type)
            deviceList = deviceobj.get_android_devices()
        for i in range(len(deviceList)):
            self.device.setItem(i, 0, QTableWidgetItem(deviceList[i]))
        self._set_device()
        mythread = device.ThreadDeviceStatus(app_type)
        mythread.trigger.connect(self._set_device_status)
        mythread.start()
        time.sleep(0.1)
        if len(deviceList) > 0:
            pack = self.get_packages()
            self.etSet.setItem(1, 1, QTableWidgetItem(str(pack)))

    def _set_device_status(self, status):
        self.device.setItem(0, 1, QTableWidgetItem(status))
        if status == "Running":
            self.device.item(0, 1).setForeground(Qt.red)
            self.statusEdit.setText("Running")
            self.startButton.setIcon(QIcon(static.runPNG))
            self.nowTime = datetime.datetime.now()
            if (self.nowTime - self.startTime).seconds > self.secsTime:
                self.stop()
        elif status == "Unreachable":
            self.device.item(0, 1).setForeground(Qt.red)
            self.statusEdit.setText("Unreachable")
            self.startButton.setIcon(QIcon(static.startPNG))
        elif status == "Connected":
            self.device.item(0, 1).setForeground(Qt.green)
            self.statusEdit.setText("Connected")
            self.startButton.setIcon(QIcon(static.startPNG))

    def del_device(self):
        """
        delete all devices
        """
        global deviceList
        deviceList = []
        common.Log.info("delete all devices")
        deviceObj = device.Device(app_type)
        deviceObj.del_device()
        for i in range(2):
            self.device.setItem(i, 0, QTableWidgetItem(""))
            for j in range(2):
                self.device.setItem(i, j, QTableWidgetItem(""))
        self.statusEdit.setText("")

    def log_show(self):
        import logShow
        self.AutoMonkeyThread = logShow.ThreadLogShow()
        self.AutoMonkeyThread.trigger.connect(self.autoMonkey_filter)
        self.AutoMonkeyThread.setup(common.logFile)
        self.AutoMonkeyThread.start()
        self.ErrorThread = logShow.ThreadLogShow()
        self.ErrorThread.trigger.connect(self.error)
        if not os.path.exists(os.path.join(self.result_path, "Error.log")):
            with open(os.path.join(self.result_path, "Error.log"), 'a') as fp:
                fp.write('ERROR')
        self.ErrorThread.setup(os.path.join(self.result_path, "Error.log"))
        self.ErrorThread.start()
        time.sleep(1)

    def checkMonkeyLog(self):
        if self.monkeyButton.text() == static.closeMonkeyLog:
            common.monkeyLogClose = True
            self.monkeyButton.setText(static.openMonkeyLog)
        else:
            import logShow
            common.monkeyLogClose = False
            self.QMonkeyThread = logShow.ThreadLogShow()
            self.QMonkeyThread.trigger.connect(self.monkey_filter)
            self.QMonkeyThread.setup(os.path.join(self.result_path, "Monkey.log"))
            self.QMonkeyThread.start()
            self.monkeyButton.setText(static.closeMonkeyLog)

    def autoMonkey_filter(self, line):
        if self.combo.currentText() == "ALL":
            self.tabwidget.mContent.textBrowser.append(line)
        elif self.combo.currentText() in line:
            self.tabwidget.mContent.textBrowser.append(line)

    def monkey_filter(self, line):
        self.tabwidget.mIndex.textBrowser.append(line)

    def error(self, line):
        self.tabwidget.mError.textBrowser.append(line+'\n')

    def exportConf(self):
        filename = common.saveConfDialog(self)
        if filename != 0:
            filepath = os.path.join(DIR, "..", "conf", filename + ".conf")
            self.set_conf(conFile=filepath)

    def importConf(self):
        times = 0
        throttle = 0
        touch = 0
        motion = 0
        lines = common.importConfDialog(self)
        if lines != "":
            if "times" in lines:
                times = lines.split("times = ")[1].split("\n")[0]
            if "throttle" in lines:
                throttle = lines.split("throttle = ")[1].split("\n")[0]
            if "touch" in lines:
                touch = lines.split("touch = ")[1].split("\n")[0]
            if "motion" in lines:
                motion = lines.split("motion = ")[1].split("\n")[0]

            hours = float('%.3f' % (float(times) * float(throttle) * 2 / (1000.0 * 60.0 * 60.0)))
            self.timeLong.setText(str(hours))
            self.etSet.setItem(0, 1, QTableWidgetItem(str(throttle)))
            # self.etPercent.setItem(0, 1, QTableWidgetItem(str(touch)))
            # self.etPercent.setItem(1, 1, QTableWidgetItem(str(motion)))

    def get_packages(self):
        deviceobj = device.Device(app_type)
        deviceList = deviceobj.get_android_devices()
        app_list = []
        if len(deviceList) > 0:
            app_content = os.popen('adb -s %s shell monkey -v -v 5' % deviceList[0])
            app_read = app_content.read()
            app_split = app_read.split('\n')
            for app in app_split:
                if app != '':
                    if 'from package' in app:
                        app = app.split('from package')[-1].replace(')', '').replace(' ','')
                        app_list.append(app)
        return app_list

    def start(self):
        self.set_conf()
        global deviceList
        if self.storOrNot():
            return
        # self.set_conf(monkeyConfFile)
        common.exitFlag = False
        common.monkeyLogClose = False
        try:
            if self.device.item(0, 1).text() == "Connected":
                try:
                    if float(self.timeLong.text()) > 0:
                        time_data = time.strftime('%Y%m%d%H%M%S', time.localtime())
                        self.result_path = os.path.join(os.getcwd(), 'Result', time_data)
                        try:
                            self.startButton.setIcon(QIcon(static.runPNG))
                            # deviceobj = device.Device(app_type)
                            # deviceList = deviceobj.get_android_devices()
                            self._set_device()
                            cf = ConfigParser.ConfigParser()
                            cf.read(monkeyConfFile)
                            deviceList = yaml.load(cf.get('Monkey', 'deviceList'))
                            flag = 1
                            self.run = runner.Runner(self.result_path, flag)
                            self.run.start(deviceList)
                            self.startTime = datetime.datetime.now()
                        except Exception as e:
                            common.Log.error(e.message)
                            common.Log.error("run error")
                        common.Log.info("start to run monkey")
                        try:
                            self.log_show()
                        except:
                            common.Log.error("log show error")
                        self.logfile.insertItem(0, time_data)
                        self.logfile.setCurrentIndex(0)
                    else:
                        common.showDialog("Message",
                                          static.dialogTimeLong)
                except:
                    common.showDialog("Message",
                                      static.dialogNoTime)
            else:
                common.showDialog("Message", static.dialogUnready)
        except:
            common.showDialog("Message", static.dialogNoDevice)

    def stop(self):
        try:
            common.Log.info("stop test")
            global deviceList
            for device in deviceList:
                os.popen('adb -s %s reboot'% device)
            self.run.stop_android()
            self.startButton.setIcon(QIcon(static.startPNG))
            common.exitFlag = True
            self.report(common.exitFlag)
            shutil.copy(common.logFile, self.result_path)
            with open(common.logFile, "w") as f:
                f.write("")
            self.statusEdit.setText("stoped")
        except Exception as e:
            common.Log.error(e.message)

    def report(self, exit=False):
        try:
            common.Log.info("create report")
            self.run.create_report(exit)
        except Exception as e:
            common.Log.error(e.message)

    def check(self):
        resultFile = os.path.join(DIR, "Result", self.logfile.currentText(), "Result.html")
        if os.path.exists(resultFile):
            self.getResult = result.ThreadGetResult()
            self.getResult.setup(resultFile)
            self.getResult.start()
        else:
            common.showDialog("information", static.dialogNoHtml)

    def storOrNot(self):
        with open(monkeyConfFile, 'r') as f:
            lines = f.read()
        try:
            if str(lines.split("--throttle = ")[1].split("\n")[0]) != self.etSet.item(0, 1).text():
                common.showDialog("Message", static.dialogNotSave)
                return True

            # if int(self.etPercent.item(0, 1).text()) != 0:
            #     if str(lines.split("touch = ")[1].split("\n")[0]) != self.etPercent.item(0, 1).text():
            #         common.showDialog("Message", static.dialogNotSave)
            #         return True
            # if int(self.etPercent.item(1, 1).text()) != 0:
            #     if str(lines.split("motion = ")[1].split("\n")[0]) != self.etPercent.item(1, 1).text():
            #         common.showDialog("Message", static.dialogNotSave)
            #         return True
            if "times" in lines:
                hours = self.timeLong.text()
                secsTime = int(float(hours) * 60 * 60)
                dlay = int(self.etSet.item(0, 1).text())
                times = str(secsTime * 1000 / (dlay * 2))
                if str(lines.split("times = ")[1].split("\n")[0]) != times:
                    common.showDialog("Message", static.dialogNotSave)
                    return True
            else:
                common.showDialog("Message", static.dialogNotSave)
        except Exception as e:
            common.Log.error(e.message)
            return True
        return False


if __name__ == '__main__':
    qt_app = QApplication(sys.argv)
    app = MainWindow()
    qt_app.exec_()

