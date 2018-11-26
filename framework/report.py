# coding:utf8
import csv
import os
import htmlmode

class Gencsv():
    def __init__(self, result_path, result):
        self.result_path = result_path
        self.result = result

    def write_result(self):
        result_file = os.path.join(self.result_path, '_result.csv')
        with open(result_file, 'ab') as csvfile:
            fieldnames = ['Time', 'Error info']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for key, value in self.result.items():
                writer.writerow({'Time': "'"+str(key), 'Error info': value})

class Htmlrepoter():
    def __init__(self, ip_list, command, result, result_path, start_time, use_time, end_time):
        self.result = result
        self.ip_list = ip_list
        self.command = command
        self.result_path = result_path
        self.start_time = start_time
        self.use_time = round(use_time / 3600,2)
        self.end_time = end_time

    def make_report(self):
        for device in self.ip_list:
            self.make_device_report(device)
            report_html = open(os.path.join(self.result_path, '%s_result.html' % device), 'w')
            report_html.write(self.tempH5)
            report_html.close()

        self.make_summery_report()
        result_html = open(os.path.join(self.result_path,'Result.html'), 'w')
        result_html.write(self.resultH5)
        result_html.close()

    def make_summery_report(self):
        h5_page = htmlmode.html_xml + htmlmode.html_head + htmlmode.html_body % (self.ip_list, str(self.command),
                                                                                 self.start_time, self.end_time,
                                                                                 self.use_time, 'Num', '报告')

        body = h5_page+htmlmode.html_sub_body %(len(self.result.keys()), '%s_result.html' % str(self.ip_list[0]),
                                                                                 '%s_result.html' % str(self.ip_list[0]))

        self.resultH5 = body + htmlmode.html_table + htmlmode.html_end % ('Report.xlsx')

    def make_device_report(self, device):
        h5_page = htmlmode.html_xml + htmlmode.html_head + htmlmode.html_body % (str(device), str(self.command),
                                                                                 self.start_time, self.end_time,
                                                                                 self.use_time,'Time','日志')
        for key, value in self.result.items():
            h5_page += '<tr class="total_row">'
            crash_package = '<td>%s</td>' % key
            h5_page += crash_package
            crash_package = '<td>core dump</td>'
            h5_page += crash_package
            h5_page += '<td><a href="%s">%s</a></td>' % (self.result_path, value)
            h5_page += '</tr>'

        self.tempH5 = h5_page + htmlmode.html_table + htmlmode.html_end % ('Report.xlsx')

if __name__ == '__main__':
    make_excel = Htmlrepoter(['192.168.64.120'], './qmonkey', {'11111111111':'2222222'},
                             'D:\workspace\monkey\\result\\20180330135925')
    make_excel.make_report()