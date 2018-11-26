# coding:utf8

html_xml = '''<?xml version="1.0" encoding="UTF-8"?>
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html xmlns="http://www.w3.org/1999/xhtml">'''

html_head  = '''
<head>
    <title>Monkey 测试结果展示</title>
    <meta name="generator" content="HTMLTestRunner 0.8.3"/>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>

    <link href="http://cdn.bootcss.com/bootstrap/3.3.0/css/bootstrap.min.css" rel="stylesheet">
</head>
'''

html_body = '''
<body>
<div id="div_base">
    <div class='page-header'>
        <div class="row">
            <div class="col-lg-12">
                <h1 class="page-header"><img src="../../source/logo.jpg">Monkey测试结果</h1>
            </div>
        </div>
        <table class="table table-bordered result_table">
        <tr class='header_row'>
        <td>设备ID</td>
        <td>%s</td>
        </tr>
        <tr class='header_row'>
        <td>命令参数</td>
        <td>%s</td>
        </tr>
        <tr class='header_row'>
        <td>开始时间</td>
        <td>%s</td>
        </tr>
        <tr class='header_row'>
        <td>结束时间</td>
        <td>%s</td>
        </tr>
        <tr class='header_row'>
        <td>执行时长</td>
        <td>%s</td>
        </tr>
        </table>
    </div>
    <h3 class='description'>ANR结果统计</h3>

    <p></p>
    <table class="table table-bordered result_table">
        <tr class='header_row'>
            <td>%s</td>
            <td>数量</td>
            <td>%s</td>
        </tr>
'''
html_crash = '<h3 class="description">CRASH结果统计</h3>' \
             '<p></p>' \
             '<table class="table table-bordered result_table">' \
             '<tr class="header_row">' \
             '<td bgcolor="#F0F0F0">%s</td>' \
             '<td bgcolor="#F0F0F0">数量</td>' \
             '<td bgcolor="#F0F0F0">%s</td>' \
             '</tr>'

html_sub_body = '''
            <tr class='total_row'>
            <!--package, packages, num, package, logpath, logpath-->
            <td>%s</td>
            <td colspan="1">core dump</td>
            <td>
                <a href="%s">%s</a>
            </td>
'''
html_tr = '</tr>'
html_table = '</table>'
html_end = '''
<p></p>
    <table class="table table-bordered result_table">
        <tr class='total_row'>
                <td>
                    <a href="%s">详情</a>
                </td>
        </tr>
    </table>
    <div id='ending'>&nbsp;</div>

</div>
</body>
</html>
'''

# report_html = open('result.html', 'w')
# report_html.write(html_xml + html_head + html_body + html_tr +html_table+ html_end)
# report_html.close()

