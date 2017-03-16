#!/usr/bin/env python
# coding=utf-8
'''
File Name: rewriteOutput.py
@Author: aidifeng
'''

import sys
import xlwt
import xlrd
import os
def writeSheetHead(sheet):
	sheet.write(0, 0, 'SKU')
	sheet.write(0, 1, '中文名称')
	sheet.write(0, 2, '图片')
	sheet.write(0, 3, '采购链接')
	sheet.write(0, 4, '尺码')
	sheet.write(0, 5, '颜色')
	sheet.write(0, 6, '含包装重量[g]')
	sheet.write(0, 7, '包装长度[cm]')
	sheet.write(0, 8, '包装宽度[cm]')
	sheet.write(0, 9, '包装高度[cm]')
	sheet.write(0, 10, '起批数量')
	sheet.write(0, 11, '采购价格')
	sheet.write(0, 12, '采购备注')
	sheet.write(0, 13, '图片网址1')
	sheet.write(0, 14, '图片网址2')
	sheet.write(0, 15, '图片网址3')
	sheet.write(0, 16, '图片网址4')

def rewriteOutput():
	reload(sys)
	sys.setdefaultencoding("utf-8")

	workbook = xlwt.Workbook(encoding = 'utf-8') 
	sheet1 = workbook.add_sheet('单属性',cell_overwrite_ok=True)
	sheet2 = workbook.add_sheet('多属性',cell_overwrite_ok=True)
	writeSheetHead(sheet1)
	writeSheetHead(sheet2)

	out = []
	data = xlrd.open_workbook('output0.xls')
	out.append(data)
	data = xlrd.open_workbook('output1.xls')
	out.append(data)
	data = xlrd.open_workbook('output2.xls')
	out.append(data)
	data = xlrd.open_workbook('output3.xls')
	out.append(data)

	cnt1 = 1
	cnt2 = 1
	for xls in out:
		ta = 1
		for table in xls.sheets():
			for i in range(table.nrows):
				for j in range(table.ncols):
					cell = table.cell(i, j).value
					if ta == 1:
						sheet1.write(cnt1, j, cell)
					if ta == 2:
						sheet2.write(cnt2, j, cell)
				if ta == 1:
					cnt1 = cnt1 + 1
				if ta == 2:
					cnt2 = cnt2 + 1
			ta = ta + 1

	workbook.save('output.xls')
	os.system('del output0.xls,output1.xls,output2.xls,output3.xls')

if __name__ == '__main__':
	rewriteOutput()
