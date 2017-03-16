#!/usr/bin/env python
# coding=utf-8
'''
File Name: run.py
@Author: aidifeng
'''

from multiprocessing.dummy import Pool as ThreadPool
from rewriteOutput import rewriteOutput
from spider import runSpider
import time
import sys

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding("utf-8")
	input_file = open('input.txt')
	lines = input_file.readlines()

	urls = []
	l = len(lines)
	l1 = int(l / 4)
	l2 = int(l / 2)
	l3 = int(l * 3 / 4)
	urls.append(lines[0:l1])
	urls.append(lines[l1:l2])
	urls.append(lines[l2:l3])
	urls.append(lines[l3:l])
	L = [1, l1 + 1, l2 + 1, l3 + 1]
	time1 = time.time()
	pool = ThreadPool(4)
	for i in range(len(urls)):
		if len(urls[i]):
			pool.apply_async(runSpider, (urls[i], i, L[i], ))
	#res = pool.map(test, urls)
	pool.close()
	pool.join()
	time2 = time.time()
	print 'Multi:' + str(time2 - time1)

	rewriteOutput()