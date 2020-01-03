import os
import csv
import xlwt
from django.conf import settings


def make_base_csv(csv_name, csv_rows):
    """生成基础excel"""

    # 判断目录是否存在,不存在则创建新目录
    cwd = os.path.join(settings.BASE_DIR, 'excel')
    if not os.path.exists(cwd):
        os.makedirs(cwd)

    # 判断文件是否存在,存在则删除
    csv_path = os.path.join(cwd, csv_name)
    if os.path.exists(csv_path):
        os.remove(csv_path)

    with open(csv_path, 'w') as f:
        csv_file = csv.writer(f)
        csv_file.writerows(csv_rows)

    return csv_path

def make_base_excel(excel_name, sheet_name, channel, start_time, end_time):
    """生成基础excel"""

    # 判断目录是否存在,不存在则创建新目录
    cwd = os.path.join(settings.BASE_DIR, 'excel')
    if not os.path.exists(cwd):
        os.makedirs(cwd)

    # 判断文件是否存在,存在则删除
    excel_path = os.path.join(cwd, excel_name)
    if os.path.exists(excel_path):
        os.remove(excel_path)

    # 创建excel文件
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(sheet_name)

    first_col = worksheet.col(0)
    first_col.width = 256 * 40

    second_col = worksheet.col(1)
    second_col.width = 256 * 40

    row = 0
    worksheet.write(row, 0, label='waf_channel:')
    worksheet.write(row, 1, label=channel)

    row += 1
    worksheet.write(row, 0, label='start_time:')
    worksheet.write(row, 1, label=start_time)

    row += 1
    worksheet.write(row, 0, label='end_time:')
    worksheet.write(row, 1, label=end_time)

    return row, excel_path, worksheet, workbook