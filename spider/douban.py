# -*- coding:utf-8 -*-

import requests
from lxml import etree
import Queue

class DouBan:
	def __init__(self):
		self.headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
		self.baseUrl = "https://movie.douban.com/top250"
		self.dataQueue = Queue.Queue()

	def loadPage(self, url):
		return requests.get(url, headers = self.headers).content

	def parsePage(self, url):
		content = self.loadPage(url)
		html = etree.HTML(content)

		# 所有的电影结点
		node_list = html.xpath("//div[@class='info']")
		
		for node in node_list:                
			# 每部电影的标题
			title = node.xpath(".//span[@class='title']/text()")[0]
			# 每部电影的评分
			score = node.xpath(".//span[@class='rating_num']/text()")[0]
			self.dataQueue.put(title + "\t" + score)

		if url == self.baseUrl:
			return [self.baseUrl + link for link in html.xpath("//div[@class='paginator']/a/@href")]

	def startWork(self):
		link_list = self.parsePage(self.baseUrl)
		for link in link_list:
			self.parsePage(link)

		while not self.dataQueue.empty():
			print self.dataQueue.get()		

def main():
	spider = DouBan()
	spider.startWork()

if __name__ == "__main__":
	main()
