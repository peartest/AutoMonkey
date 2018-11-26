# coding:utf8
import threading
import os, re
import time
import sys
import yaml
sys.path.append('..')
import genexcel
import htmlreport
from common import logging_manager
from common import common
from AutoBot import LinuxTestLibrary
import subprocess
import report
import logging
import ConfigParser
timeout =1

class AndroidRunner():
    def __init__(self, ip_list, command, result_path):
        self.ip_list = ip_list
        self.result = {}
        self.command = command
        self.result_path = result_path
        self.start_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        self.start_data = time.time()

    def run(self):
        if not os.path.exists(self.result_path):
            try:
                os.mkdir(self.result_path)
            except:
                os.makedirs(self.result_path)
        thread_list = []
        for ip in self.ip_list:
            packages = get_packages(ip)
            run_device = RunAndroidThread(self.result_path, ip, packages, self.result, self.command)
            thread_list.append(run_device)
            run_device.start()

    def stop(self):
        global timeout
        timeout = 0

class RunAndroidThread(threading.Thread):
    def __init__(self, result_path, device, packages, result, command):
        threading.Thread.__init__(self)
        self.device = device
        self.packages = packages
        self.result = result
        self.result_path = result_path
        self.command = command


    def run(self):
        thread_list = []
        start_time = time.time()
        time_data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        print self.command
        run_time_out = self.command.split(';')[-1]
        global timeout
        timeout =  start_time + int(run_time_out)
        try:
            # time_end = timeout - time.time()
            while time.time() < timeout:
                for app in self.packages:
                    try:
                        if self.device not in self.result.keys():
                            self.result[self.device] = {}
                        run_monkey = MonkeyRunner(self.result_path, self.device, app,
                                                  self.result[self.device], self.command)
                        thread_list.append(run_monkey)
                        run_monkey.start()
                        app_starttime = time.time()
                        for t in thread_list:
                            t.join()
                        pwd = os.getcwd()
                        # os.chdir(self.result_path)
                        genexcel.Excel(self.result_path, self.result).report()
                        self.result[self.device]['time'] = (time.time() - start_time)/3600
                        htmlreport.Htmlreport(self.result, time_data, self.result_path, '', self.packages).make_report()
                        os.chdir(pwd)
                    except:
                        pass
                    if time.time() > timeout:
                        break
                # time_end = timeout - time.time()

        except Exception as e:
            logging.debug(e)
        finally:
            logging.info('****************************************************')
            logging.info('%s test finished '% (self.device))
            logging.info('%s all runtime %s s' % (self.device, time.time() - start_time))
            logging.info('****************************************************')

class MonkeyRunner(threading.Thread):
    def __init__(self, result_path, device, package, result, command):
        threading.Thread.__init__(self)
        self.package = package
        self.device = device
        self.result_path = result_path
        self.result = result
        self.command = command

    def run(self):
        monkey(self.result_path, self.device, self.package, self.result, self.command)

def get_packages(device):
    cf = ConfigParser.ConfigParser()
    monkeyConfFile = common.defaultConf
    cf.read(monkeyConfFile)
    app_list = cf.get('Monkey', 'package')
    app_list = yaml.load(app_list)
    return app_list

def monkey(result_path, device, monkey_package, result, command):
    # get monkey command
    command = command.split(';')[0]
    device_path = os.path.join(result_path, device)
    if not os.path.exists(device_path):
        try:
            os.mkdir(device_path)
        except:
            os.makedirs(device_path)
    display_log = logging_manager.Logger(os.path.join(result_path, 'Monkey.log'))
    log = logging_manager.Logger(os.path.join(result_path, '%sMonkey.log'%device))
    monkey_command = 'adb -s %s shell monkey -p '%device + monkey_package + ' --pct-anyevent 0'
    monkey_command = monkey_command + ' --ignore-crashes'
    monkey_command = monkey_command + ' --ignore-timeouts'
    monkey_command = monkey_command + ' --kill-process-after-error'
    monkey_command = monkey_command + ' --ignore-security-exceptions'
    monkey_command = monkey_command + ' --pct-syskeys 0 '
    monkey_command = monkey_command + command + ' -v -v -v ' + str(3000)

    popen = subprocess.Popen(monkey_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        next_line = popen.stdout.readline()
        if next_line == '' and popen.poll() != None:
            break
        else:
            log.info(next_line)
            display_log.info(next_line)
            if next_line.find('CRASH') != -1:
                with open(os.path.join(result_path, 'Error.log'), 'a') as fp:
                    fp.write(next_line)
                time_data = time.strftime('%Y%m%d%H%M%S', time.localtime())
                crash_popen = subprocess.Popen('adb -s %s logcat -d -v threadtime *:V'%device,
                                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    pack_name = re.search('CRASH:\s(.*?)\s\(pid', next_line).group(1)
                except:
                    pack_name = monkey_package
                if pack_name not in result.keys():
                    result[pack_name] = {}
                log_path = os.path.join(device_path, pack_name, 'Crash',time_data)
                if not os.path.exists(log_path):
                    try:
                        os.mkdir(log_path)
                    except:
                        os.makedirs(log_path)
                with open(os.path.join(log_path, 'MonkeyCrashError.log'), 'a') as fp:
                    fp.write(next_line)
                crash_log_file = open(os.path.join(log_path, '%sCRASH.log' % (pack_name)), 'a')
                while True:
                    next_line = crash_popen.stdout.readline()
                    if next_line == '' and crash_popen.poll() != None:
                        break
                    else:
                        crash_log_file.write(next_line + '\n')
                crash_log_file.close()
                crash_popen.terminate()
                try:
                    result[pack_name]['Crash'] += 1
                except:
                    result[pack_name]['Crash'] = 1
            if next_line.find('NOT RESPONDING') != -1:
                with open(os.path.join(result_path, 'Error.log'), 'a') as fp:
                    fp.write(next_line)
                time_data = time.strftime('%Y%m%d%H%M%S', time.localtime())
                anr_popen = subprocess.Popen('adb -s %s logcat -d -v threadtime *:V'%device,
                                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    pack_name = re.search('NOT RESPONDING:\s(.*?)\s\(pid', next_line).group(1)
                except:
                    pack_name = monkey_package
                if pack_name not in result.keys():
                    result[pack_name] = {}
                log_path = os.path.join(device_path, pack_name, 'ANR', time_data)
                if not os.path.exists(log_path):
                    try:
                        os.mkdir(log_path)
                    except:
                        os.makedirs(log_path)
                with open(os.path.join(log_path, 'MonkeyANRError.log'), 'a') as fp:
                    fp.write(next_line)
                anr_log_file = open(os.path.join(log_path, '%sANR.log' % (pack_name)), 'a')
                while True:
                    next_line = anr_popen.stdout.readline()
                    if next_line == '' and anr_popen.poll() != None:
                        break
                    else:
                        anr_log_file.write(next_line + '\n')
                anr_log_file.close()
                anr_popen.terminate()
                pull_trace = subprocess.Popen('adb -s %s pull /data/anr %s' % (device, log_path),
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                pull_trace = subprocess.Popen('adb -s %s shell rm -rf  /data/anr/*' % (device),
                                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                try:
                    result[pack_name]['ANR'] += 1
                except:
                    result[pack_name]['ANR'] = 1


class Runner():
    def __init__(self, ip_list, command, result_path):
        self.ip_list = ip_list
        self.result = {}
        self.command = command
        self.result_path = result_path
        self.start_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        self.start_data = time.time()

    def run(self):
        if not os.path.exists(self.result_path):
            try:
                os.mkdir(self.result_path)
            except:
                os.makedirs(self.result_path)
        thread_list = []
        for ip in self.ip_list:
            run_device = RunDeviceThread(self.result_path, ip, self.result, self.command)
            thread_list.append(run_device)
            run_device.start()

    def create_report(self):
        self.use_time = time.time() - self.start_data
        self.end_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime())
        gen = report.Gencsv(self.result_path, self.result)
        gen.write_result()
        html_report = report.Htmlrepoter(self.ip_list, self.command, self.result, self.result_path,
                                         self.start_time, self.use_time, self.end_time)
        html_report.make_report()

class RunDeviceThread(threading.Thread):
    def __init__(self, result_path, ip, result, command):
        threading.Thread.__init__(self)
        self.ip = ip
        self.result = result
        self.result_path = result_path
        self.command = command
        self.log = logging_manager.Logger(os.path.join(self.result_path, 'Monkey.log'))
        self.keep = True
        self.line = ''
        self.out_info =""
        self.err_info =""


    def print_log(self, out, err):
        if out is not None:
            self.out_info += out
            out_info = self.out_info
            outs = out_info.split("\n")
            for line in outs:
                self.log.info(line)
                self.catch_log(line, 'CRASH')
                # sys.stdout.write(line + "\n")
                # sys.stdout.flush()
                if line.count("qmonkey finish") == 1:
                    self.keep = False
        if err is not None:
            self.err_info += err
            err_info = self.err_info
            errs = err_info.split("\n")
            for line in errs:
                sys.stderr.write(line)
                sys.stderr.flush()
        self.out_info = ""
        self.err_info = ""

    def catch_sys_log(self, out, err):
        if out is not None:
            if out != "\n":
                self.line += out
            else:
                self.journalctl_log.info(self.line)
                self.line = ''
        if err is not None:
            sys.stderr.write(err)
            sys.stderr.flush()

    def catch_log(self, line, str):
        if line.find(str) != -1:
            try:
                with open(os.path.join(self.result_path, 'Error.log'), 'a') as fp:
                    fp.write(line)
                time_data = time.strftime('%Y%m%d%H%M%S', time.localtime())
                self.result[time_data] = line
                log_path = os.path.join(self.result_path, time_data)
                if not os.path.exists(log_path):
                    os.mkdir(log_path)
                autobot_lib = LinuxTestLibrary()
                autobot_lib.connect_to_device_ssh(self.ip)
                self.journalctl_log = logging_manager.Logger(os.path.join(log_path, 'journalctl.log'))
                autobot_lib.exec_ssh_cmd('journalctl -b', shell=True, func=self.catch_sys_log)
                time.sleep(5)
                autobot_lib.cur_connector.close_shell()  # 最好先close
                autobot_lib.disconnect_device_ssh()
                self.get_logfile(line, log_path)
            except Exception as e:
                self.log.error(e)

    def keep_run(self):
        while self.keep:
            pass

    def connect_device(self):
        self.testlib = LinuxTestLibrary()
        self.testlib.connect_to_device_ssh(self.ip)

    def run_ssh(self):
        res = self.testlib.exec_ssh_cmd(self.command, shell=True, func=self.print_log)

    def get_logfile(self, str, path):
        try:
            target_log_path = str.split('[Coredump]')[-1].split('[')[0]
        except:
            target_log_path = '/tmp/coredump-*'
        target_log_name = target_log_path.split('/')[-1].replace(':', '_')
        self.copy_file(target_log_path, os.path.join(path, target_log_name))

    def copy_file(self, src, dst):
        autobot_lib = LinuxTestLibrary()
        try:
            autobot_lib.connect_to_device_ssh(self.ip)
        except Exception as e:
            self.log.warning(e)
        try:
            autobot_lib.scp_get_file(src, dst, ip = self.ip)
        except Exception as e:
            self.log.warning(e)
        autobot_lib.disconnect_device_ssh()

    def run(self):
        self.connect_device()
        self.run_ssh()
        self.keep_run()

if __name__ == '__main__':
    a = AndroidRunner(['19a17054'], '--throttle 1000,20', 'D:\\workspace\\AutoMonkey\\Result\\20180530140732')
    a.run()



