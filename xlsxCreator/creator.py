import xlsxwriter

if __name__ == '__main__':
    workbook = xlsxwriter.Workbook('result.xlsx')
    worksheet = workbook.add_worksheet('report')
    worksheet.write('A1', 'phone')
    for i in range(2, 500002):
        worksheet.write('A'+str(i), '0100{:07d}'.format(i))
    workbook.close()
'''
    worksheet.write('A1', 'name')
    worksheet.write('B1', 'phone')

    worksheet.write('A'+str(i), '홍'+str(i))
    worksheet.write('B'+str(i), '0100{:07d}'.format(i))
'''
