'''
合并单元格，居中

'''

import xlsxwriter
# 导出文件使用的模块
from io import StringIO

# # @app.route('/down_excel')
# def down_excel():
#     sio = StringIO()
#     workbook = xlsxwriter.Workbook(sio)  # 直接写到io中
#     sheet = workbook.add_worksheet(u'sheet1')
#     style = workbook.add_format()  # 设置风格
#     sheet.merge_range(0, 0, 0, 5, 'aaa')  # 合并单元格
#     sheet.write('A2', u'内容', style)
#     for i in range(2, 10):
#         sheet.write(i, 2, 1)
#     sheet.write(11, 2, '=SUM(1:10)')  # 增加公式
#     sheet.set_column(0, 5, 10)  # 设置列宽
#     sheet.set_default_row(35)  # 设置默认行高
#     workbook.close()  # 需要关闭
#     # sio.seek(0)  # 找到流的起始位置
#     # resp = make_response(sio.getvalue())
#     # resp.headers["Content-Disposition"] = "attachment; filename={}.xlsx".format('name')
#     # resp.headers['Content-Type'] = 'application/x-xlsx'
#     # return resp

def xlsx_style(**kwargs):
    style = {
        # 'bold': kwargs.get('bold', False),  # 加粗
        # 'font_name': kwargs.get('font_name', 'SimSun'),  # 字体类型，默认宋体
        # 'font_size': kwargs.get('font_size', 12),  # 字体大小，默认12
        # 'font_color': kwargs.get('font_color', '#000000'),  # 字体颜色，黑色
        'align': kwargs.get('align', 'center'),  # 默认水平居中
        'valign': kwargs.get('valign', 'vcenter'),  # 默认垂直居中
        # 'text_wrap': kwargs.get('text_wrap', True),  # 默认自动换行
        'top': kwargs.get('top', 1),  # 上边界，线条宽度
        'bottom': kwargs.get('bottom', 1),  # 边界
        'left': kwargs.get('left', 1),  # 边界
        'right': kwargs.get('right', 1),  # 边界
        'bg_color': kwargs.get('bg_color', '#FFFFFF'),  # 背景颜色，白色
        # 其他类型设置格式可以接着写
    }

    return style

# head_style = workbook.add_format(xlsx_style(bold=True, font_size=20))
# body_style = workbook.add_format(xlsx_style(bg_color='#FFFF00'))
# center_style = workbook.add_format(xlsx_style(align='center', valign='vcenter'))
# worksheet.write(2, 5, 'aaa', body_style)

