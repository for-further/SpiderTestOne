#!/usr/bin/env python
# coding=utf-8
'''
File Name: spider.py
@Author: aidifeng
'''

from lxml import etree
from click import click
import requests
import datetime
import time
import xlwt
import json
import sys


def getTitle(selector):
	title = selector.xpath('//title/text()')
	return title[0]

def getImages(selector):
	content = selector.xpath('//ul[@class="nav nav-tabs fd-clr"]/li')
	imgs = []
	for i in content:
		info = json.loads(i.xpath('@data-imgs')[0])
		imgs.append(info['original'])
	return imgs

def getPriceAndBegin(selector):
	content = selector.xpath('//div[@class="widget-custom-container"]/script[@type="text/javascript"]/text()')
	info = content[0].replace('\n', '').replace('\t', '').replace(' ', '')
	iDetailConfig = info.split(';v')[0].split('variDetailConfig=')[1]
	#iDetailConfig = info[0].split('variDetailConfig=')[1].split(',\'end\'')[0]
	#iDetailConfig = iDetailConfig + '}'
	iDetailConfig = json.loads(iDetailConfig.replace('\'', '"'))
	price = iDetailConfig['refPrice']
	begin = iDetailConfig['beginAmount']

	try:
		dis = info.split('"discount":"')[-1]
		discount = dis.split('"')[0]
		#discount = iDetailConfig['discount']
		price = str(float(price) * float(discount))
	except:
		print "NO Discount"
		#print info
	return price, begin
'''
def getPriceAndBegin(selector):
	content = selector.xpath('//div//table//td[@data-range]')
	#print len(content)
	info = json.loads(content[0].xpath('@data-range')[0])
	#print info
	price = info['price']
	begin = info['begin']
	return price, begin'''

def getColor(selector):
	content = selector.xpath('//ul[@class="list-leading"]/li/div')
	color = []
	if len(content):
		for i in content:
			info = i.xpath('@data-unit-config')[0].replace('"', '').replace('{', '').replace('}', '').split(':')
			color.append(info[1])
	return color

def getSize(selector):
	content = selector.xpath('//table[@class="table-sku"]//tr[@data-sku-config]')
	size = []
	if len(content):
		for i in content:
			info = json.loads(i.xpath('@data-sku-config')[0])
			size.append(info['skuName'])

	content = selector.xpath('//table[@class="table-sku"]//td[@class="price"]//em[@class="value"]/text()')
	prices = []
	if len(content):
		for i in content:
			prices.append(i);

	return size, prices


def writeSheet(sheet, imgs, url, sz, col, weight, length, width, height, begin, price, cnt):
	sheet.write(cnt, 2, imgs[0])
	sheet.write(cnt, 3, url)
	sheet.write(cnt, 4, sz)
	sheet.write(cnt, 5, col)
	sheet.write(cnt, 6, weight)
	sheet.write(cnt, 7, length)
	sheet.write(cnt, 8, width)
	sheet.write(cnt, 9, height)
	sheet.write(cnt, 10, begin)
	sheet.write(cnt, 11, price)
	k = 13
	for i in imgs:
		sheet.write(cnt, k, i)
		k = k + 1

def Spider(url, idx, cnt1, cnt2, sheet1, sheet2):
	html = requests.get(url);
	selector = etree.HTML(html.text)
	title = getTitle(selector)
	#print title
	imgs = getImages(selector)
	#print imgs
	price, begin = getPriceAndBegin(selector)
	#print price, begin
	color = getColor(selector)
	#print color
	size, prices = getSize(selector)
	#print size, prices
	length = '10'
	height = '10'
	width = '10'

	weight, freight = click(url)

	
	if len(color) and len(size):
		for c in color:
			id = 0
			for s in size:
				remark = c + '-' + s;
				sheet2.write(cnt2, 0, idx + '-' + remark)
				sheet2.write(cnt2, 1, title + '-' + remark)
				writeSheet(sheet2, imgs, url, s, c, weight, length, width, height, begin, str(float(prices[id]) + float(freight)), cnt2)
				sheet2.write(cnt2, 12, remark)
				cnt2 = cnt2 + 1
				id = id + 1
	elif len(color):
		for c in color:
			remark = c;
			sheet2.write(cnt2, 0, idx + '-' + remark)
			sheet2.write(cnt2, 1, title + '-' + remark)
			writeSheet(sheet2, imgs, url, '', c, weight, length, width, height, begin, str(float(price) + float(freight)), cnt2)
			sheet2.write(cnt2, 12, remark)
			cnt2 = cnt2 + 1
	elif len(size):
		id = 0
		for s in size:
			remark = s;
			sheet2.write(cnt2, 0, idx + '-' + remark)
			sheet2.write(cnt2, 1, title + '-' + remark)
			writeSheet(sheet2, imgs, url, s, '', weight, length, width, height, begin, str(float(prices[id]) + float(freight)), cnt2)
			sheet2.write(cnt2, 12, remark)
			cnt2 = cnt2 + 1
			id = id + 1
	else:
		sheet1.write(cnt1, 0, idx)
		sheet1.write(cnt1, 1, title)
		writeSheet(sheet1, imgs, url, '', '', weight, length, width, height, begin, str(float(price) + float(freight)), cnt1)
		cnt1 = cnt1 + 1;

	return cnt1, cnt2;


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

def runSpider(urls, file_idx, sku_idx):
	reload(sys)
	sys.setdefaultencoding("utf-8")
	now = datetime.datetime.now()
	now = now.strftime('%y%m%d') 

	workbook = xlwt.Workbook(encoding = 'utf-8') 
	sheet1 = workbook.add_sheet('sheet1',cell_overwrite_ok=True)
	sheet2 = workbook.add_sheet('sheet2',cell_overwrite_ok=True)
	#writeSheetHead(sheet1)
	#writeSheetHead(sheet2)

	cnt1 = 0
	cnt2 = 0
	for url in urls:
		print sku_idx
		idx = now + str(sku_idx).zfill(4)
		cnt1, cnt2 = Spider(url, idx, cnt1, cnt2, sheet1, sheet2)
		sku_idx = sku_idx + 1

	workbook.save('output' + str(file_idx) + '.xls')


if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	now = datetime.datetime.now()
	now = now.strftime('%y%m%d') 
	input_file = open('input.txt')
	lines = input_file.readlines()

	workbook = xlwt.Workbook(encoding = 'utf-8') 
	sheet1 = workbook.add_sheet('单属性',cell_overwrite_ok=True)
	sheet2 = workbook.add_sheet('多属性',cell_overwrite_ok=True)
	writeSheetHead(sheet1)
	writeSheetHead(sheet2)
	
	time1 = time.time()
	cnt1 = 1
	cnt2 = 1
	i = 1
	for url in lines:
		print i
		idx = now + str(i).zfill(4)
		cnt1, cnt2 = Spider(url, idx, cnt1, cnt2, sheet1, sheet2)
		i = i + 1

	workbook.save('output.xls')
	input_file.close()
	time2 = time.time()
	print 'single time:' + str(time2 - time1)

