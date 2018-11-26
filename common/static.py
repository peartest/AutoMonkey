#!/usr/bin/env python
# -*- coding:utf-8 -*-
from PySide.QtCore import QTextCodec
import os
codec = QTextCodec.codecForName("utf-8")
title = codec.toUnicode("TMonkey")
deviceString = codec.toUnicode("设备状态：")
timeString = codec.toUnicode("计划执行时长：")
eventTypeSet = codec.toUnicode("事件类型设置：")
eventTpyePercent = codec.toUnicode("事件类型百分比：")
storeButton = codec.toUnicode("保存")
cancleButton = codec.toUnicode("取消")
startButton = codec.toUnicode("开始")
stopButton = codec.toUnicode("停止")
status = codec.toUnicode("运行状态：")
checkLog = codec.toUnicode("查看")
menuFile = codec.toUnicode("文件")
importFile = codec.toUnicode("导入")
exportFile = codec.toUnicode("导出")
menuHelp = codec.toUnicode("帮助")
package = codec.toUnicode("包配置")
menuAbout = codec.toUnicode("关于")
dialogAbout = codec.toUnicode("""软件版本：V1.2.1\nQmonkey 版本：V0.2.3""")
menuSet = codec.toUnicode("设置")
pcSet = codec.toUnicode("PC环境设置")
logInfo = codec.toUnicode("日志：")
selectlog = codec.toUnicode("测试报告：")
logFilter = codec.toUnicode("日志过滤：")
findDeviceButton = codec.toUnicode("查找并连接设备")
deleteDeviceButton = codec.toUnicode("删除设备")
deviceName = codec.toUnicode("设备")
timeLong = codec.toUnicode("运行时长")
logShow = codec.toUnicode("运行log显示")
parameter = codec.toUnicode("参数值设置")
openMonkeyLog = codec.toUnicode("monkey运行日志")
closeMonkeyLog = codec.toUnicode("关闭monkey运行日志")
dialogNoDevice = codec.toUnicode("设备未准备好")
dialogNoTime = codec.toUnicode("未填写monkey执行时长")
dialogSetTime = codec.toUnicode("请设置monkey执行时长")
dialogUnready = codec.toUnicode("设备未准备好")
dialogTimeLong = codec.toUnicode("执行时长应该大于0")
dialogNoHtml = codec.toUnicode("未发现Result.html文件")
dialogStorDefaultConf = codec.toUnicode("文件保存成功")
dialogStoreNewFile = codec.toUnicode("新文件保存成功")
dialogNotSave = codec.toUnicode("参数设置未保存")


nowPath = os.getcwd()
sourcePath = os.path.join(nowPath, 'source')
importPNG = os.path.join(sourcePath, 'import.png')
exportPNG = os.path.join(sourcePath, 'export.png')
findDevice = os.path.join(sourcePath, 'findDevice.png')
androidDevice = os.path.join(sourcePath, 'androidDevice.png')
deleteDevice = os.path.join(sourcePath, 'deleteDevice.png')
runPNG = os.path.join(sourcePath, 'run.png')
startPNG = os.path.join(sourcePath, 'start.png')
stopPNG = os.path.join(sourcePath, 'stop.png')
storePNG = os.path.join(sourcePath, 'store.png')
setPNG = os.path.join(sourcePath, 'set.png')

logLevel = ('ALL', 'INFO', 'WARN', 'ERROR', 'DEBUG')

eventType = {"--throttle": "500"}
eventPercent = {"--pct-touch": "0", "--pct-motion": "0"}
times = "0"

resultPath = os.path.join(nowPath, "Result")


