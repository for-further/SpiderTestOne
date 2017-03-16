#!/usr/bin/env python
# coding=utf-8
'''
File Name: click.py
@Author: aidifeng
'''

from selenium import webdriver
from lxml import etree
import time
import sys

def click(url):
	freight = '0'
	weight = '0'
	pwd = './phantomjs.exe'
	#print pwd
	driver = webdriver.PhantomJS(executable_path=pwd)
	#driver = webdriver.Firefox();
	driver.get(url)
	try:
		link = driver.find_element_by_xpath('//a[@class="parcel-location"]')
		link.click()
		time.sleep(2)
		html = driver.page_source
		#print html

		selector = etree.HTML(html)
		content = selector.xpath('//span[@class="parcel-unit-weight"]/span[@class="value"]/text()')
		weight = content[0]
		weight = str(int(float(weight) * 1000.0))
		#print weight

		link = driver.find_element_by_xpath('//a[@title="浙江"]')
		link.click()
		time.sleep(2)
		html = driver.page_source
		#print html

		link = driver.find_element_by_xpath('//a[@title="金华"]')
		link.click()
		time.sleep(2)
		html = driver.page_source
		#print html

		selector = etree.HTML(html)
		content = selector.xpath('//div[@class="cost-entries-type"]//em/text()')
		if len(content):
			freight = content[0]
		#print freight
	except:
		pass


	driver.close()

	return weight, freight




if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	url = 'https://detail.1688.com/offer/527358843426.html'
	click(url)