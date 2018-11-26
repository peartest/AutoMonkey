#-*- encoding:UTF-8 -*-
import os
import xlsxwriter
import yaml

class Excel():
    def __init__(self, result_path, dic):
        self.result_path = result_path
        self.dic = dic

    def report(self):
        report_path = os.path.join(self.result_path, 'Report.xlsx')
        try:
            if os.path.exists(report_path):
                os.remove(report_path)
            workbook = xlsxwriter.Workbook(report_path)
            self.write_report(workbook)
            workbook.close()
        except:
            pass

    def write_report(self, workbook):
        worksheet = workbook.add_worksheet('Summery')
        worksheet.write('A1', 'Package')
        for i in range(len(self.dic.keys())):
            worksheet.write(0, i+1, self.dic.keys()[i])
            j = 0
            for pack in self.dic[self.dic.keys()[i]]:
                if pack == 'time':
                    continue
                j += 1
                worksheet.write('A%s' % (j + 1), pack)
                try:
                    worksheet.write(j , i+1, self.dic[self.dic.keys()[i]][pack]['Crash'])
                except:
                    worksheet.write(j, i+1, 0)
            crash_count = 0
            for key, value in self.dic[self.dic.keys()[i]].items():
                try:
                    crash_count += self.dic[self.dic.keys()[i]][key]['Crash']
                except:
                    crash_count += 0
            worksheet.write(j+1, i + 1, crash_count)
            worksheet.write('A%s' % (j + 2), 'Crash Summary')


            for pack in self.dic[self.dic.keys()[i]]:
                if pack == 'time':
                    continue
                worksheet.write('A%s' % (j + 4), pack)
                try:
                    worksheet.write(j+3, i+1, self.dic[self.dic.keys()[i]][pack]['ANR'])
                except:
                    worksheet.write(j+3, i+1, 0)
                j += 1
            anr_count = 0
            for key, value in self.dic[self.dic.keys()[i]].items():
                try:
                    anr_count += self.dic[self.dic.keys()[i]][key]['ANR']
                except:
                    anr_count += 0
            worksheet.write(j + 3, i + 1, anr_count)
            worksheet.write('A%s' % (j + 4), 'ANR Summary')

class MemeryExcel():
    def __init__(self, result_path, device, sys_dic):
        self.device = device
        self.sys_dic = sys_dic
        self.result_path = result_path

    def report(self):
        if os.path.exists(os.path.join(self.result_path, '%s_Memery_Report.xlsx' % (self.device))):
            os.remove(os.path.join(self.result_path, '%s_Memery_Report.xlsx' % (self.device)))
        workbook = xlsxwriter.Workbook(os.path.join(self.result_path, '%s_Memery_Report.xlsx' % (self.device)))
        self.sys_report(workbook)
        workbook.close()

    def sys_report(self, workbook):
        worksheet = workbook.add_worksheet('Summery')
        worksheet.write('A1', 'Time')
        i = 0
        for time_data in self.sys_dic:
            i += 1
            j = 0
            worksheet.write('A%s'%(i+1), time_data)
            for sys_data in self.sys_dic[time_data]:
                j += 1
                worksheet.write(0, j, sys_data)
                worksheet.write(i, j, int(self.sys_dic[time_data][sys_data]))
            j = 0

        chart = workbook.add_chart({'type': 'line'})
        # Configure series.
        chart.add_series({
            'name': ['Summery', 0, 1],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 1, len(self.sys_dic), 1],
        })

        chart.add_series({
            'name': ['Summery', 0, 2],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 2, len(self.sys_dic), 2],
        })

        chart.add_series({
            'name': ['Summery', 0, 3],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 3, len(self.sys_dic), 3],
        })

        chart.add_series({
            'name': ['Summery', 0, 4],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 4, len(self.sys_dic), 4],
        })

        chart.add_series({
            'name': ['Summery', 0, 5],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 5, len(self.sys_dic), 5],
        })

        chart.add_series({
            'name': ['Summery', 0, 6],
            'categories': ['Summery', 1, 0, len(self.sys_dic), 0],
            'values': ['Summery', 1, 6, len(self.sys_dic), 6],
        })
        # Add a chart title and some axis labels.
        chart.set_title({'name': 'Memory Monitor'})
        chart.set_x_axis({'name': 'Time'})
        chart.set_y_axis({'name': 'Memory (kB)'})

        # Set an Excel chart style. Colors with white outline and shadow.
        chart.set_style(10)

        # Insert the chart into the worksheet (with an offset).
        try:
            worksheet.insert_chart('H2', chart)
        except Exception as e:
            print e

if __name__ == '__main__':
    fp = open('Summary.txt', 'r')
    result = yaml.load(fp.read())
    make_excel = Excel(result)
    make_excel.report()


