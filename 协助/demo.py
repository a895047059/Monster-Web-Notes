
import os
import xlrd
import pandas as pd

path = './data'
if not os.path.exists(path):
    os.mkdir(path)

pathes = [i for i in os.walk(path)]
file_names = pathes[0][2]
root = pathes[0][0]
data = []
for file_name in file_names:
    abs_path = '{}/{}'.format(root, file_name)
    wb = xlrd.open_workbook(filename=abs_path)

    for sheet in wb.sheets():
        date_time = sheet.row_values(10, 0, -1)[2]
        for i in range(16, sheet.nrows):
            data.append([date_time, sheet.name] + sheet.row_values(i, 0, -1)[:8])

df = pd.DataFrame(data)
df.to_excel('./所有数据.xlsx')
