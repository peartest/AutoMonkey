# coding:utf8
import htmlmode
import yaml
import time
import os
class Htmlreport():
    def __init__(self, dic, starttime, run_path, black_list, white_list):
        self.dic = dic
        self.command = ''
        self.starttime = starttime
        self.run_path = run_path
        self.alltime = 0
        self.black_list = black_list
        self.white_list = white_list

    def make_report(self):
        for device in self.dic.keys():
            self.make_device_Template(device)
            report_html = open(os.path.join(self.run_path,'%s_result.html'%device), 'w')
            report_html.write(self.tempH5)
            report_html.close()
            try:
                self.alltime += self.dic[device]['time']
            except:
                self.alltime += 0


        self._loadTemplate()
        result_html = open(os.path.join(self.run_path, 'Result.html'), 'w')
        result_html.write(self.resultH5)
        result_html.close()

    def make_device_Template(self, device):
        try:
            self.runtime = self.dic[device]['time']
        except:
            self.runtime = 0
        command = 'adb shell monkey -p package  --pct-anyevent 0  --ignore-crashes  --ignore-timeouts ' \
                  '--kill-process-after-error  --ignore-security-exceptions  --pct-syskeys 0 1000  -v -v -v 20000'
        time_data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        h5_page = htmlmode.html_xml + htmlmode.html_head +htmlmode.html_body %(device, command, self.starttime,time_data,
                                                                               self.runtime, 'package', '日志')
        for key, value in self.dic[device].items():
            h5_page += '<tr class="total_row">'
            if key == 'time':
                continue
            anr_package = '<td>%s</td>'%key
            h5_page += anr_package
            try:
                anr_num = '<td>%s</td>'% self.dic[device][key]['ANR']
                h5_page += anr_num
            except:
                anr_num = '<td>%s</td>' % 0
                h5_page += anr_num

            h5_page +=  '<td><a href=".//%s">%s</a></td>' %(device, self.run_path)
            h5_page += '</tr>'
        h5_page = h5_page + htmlmode.html_table+ htmlmode.html_crash % ('package', '详情')
        for key, value in self.dic[device].items():
            h5_page += '<tr class="total_row">'
            if key == 'time':
                continue
            crash_package = '<td>%s</td>' % key
            h5_page += crash_package
            try:
                crash_num = '<td>%s</td>' % self.dic[device][key]['Crash']
                h5_page += crash_num
            except:
                crash_num = '<td>%s</td>' % 0
                h5_page += crash_num
            h5_page += '<td><a href=".//%s">%s</a></td>' % (device, self.run_path)
            h5_page += '</tr>'

        self.tempH5 = h5_page + htmlmode.html_table + htmlmode.html_end % ('Report.xlsx')

    def _loadTemplate(self):
        command = 'adb shell monkey -p package  --pct-anyevent 0  --ignore-crashes  --ignore-timeouts ' \
                  '--kill-process-after-error  --ignore-security-exceptions  --pct-syskeys 0 1000  -v -v -v 20000'

        time_data = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        h5_page = htmlmode.html_xml + htmlmode.html_head + htmlmode.html_body % (self.dic.keys(), command,self.starttime,
                                                                                 time_data,self.alltime, 'Device id',
                                                                                 '详情')
        crash_count = 0
        anr_count = 0
        for device in self.dic.keys():
            h5_page += '<tr class="total_row">'
            h5_page += '<td>%s</td>' % device
            for pack in self.dic[device].keys():
                try:
                    anr_count += self.dic[device][pack]['ANR']
                except:
                    anr_count += 0
            h5_page += '<td>%s</td>' % anr_count
            anr_count = 0
            device_url = device + '_result.html'
            h5_page += '<td><a href="%s">%s</a></td>' % (device_url, device_url)
            h5_page += '</tr>'

        h5_page = h5_page + htmlmode.html_table + htmlmode.html_crash % ('Device id', '详情')
        for device in self.dic.keys():
            h5_page += '<tr class="total_row">'
            h5_page += '<td>%s</td>' % device
            for pack in self.dic[device].keys():
                try:
                    crash_count += self.dic[device][pack]['Crash']
                except:
                    crash_count += 0
            h5_page += '<td>%s</td>' % crash_count
            crash_count = 0
            device_url = device + '_result.html'
            h5_page += '<td><a href="%s">%s</a></td>' % (device_url, device_url)
            h5_page += '</tr>'

        self.resultH5 = h5_page + htmlmode.html_table + htmlmode.html_end % ('Report.xlsx')


if __name__ == '__main__':
    fp = open('Summary.txt', 'r')
    result = yaml.load(fp.read())
    make_excel = Htmlreport(result, time.time(), 5, 'D:\workspace\monkey\\result\\20180330135925', [], [])
    make_excel.make_report()
