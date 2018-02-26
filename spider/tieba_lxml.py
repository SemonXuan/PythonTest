# -*- coding: utf-8 -*-
import urllib
import urllib2
from lxml import etree

class TiebaImage:
	def __init__(self):
		# 请求报头
		self.headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
		self.xpath_url = "//div[@class='t_con cleafix']/div/div/div/a/@href"
		self.xpath_image = "//img[@class='BDE_Image']/@src"
		# 固定url部分
		self.baseUrl = "https://tieba.baidu.com"
		self.tiebaName = raw_input("请输入贴吧名：")
		self.startPage = int(raw_input("请输入起始页："))
		self.endPage = int(raw_input("请输入终止页："))

	def loadRequest(self, url):
		"""
			作用：发送url请求，返回响应
			url：页面的url地址
		"""
		# 构建请求对象
		request = urllib2.Request(url, headers = self.headers)
		# 发送请求，返回响应
		try:
			response = urllib2.urlopen(request)
			html = response.read()
			return html
		except RuntimeError, e:
			print(e.message)
			print("[ERR]：下载失败")

	def dealPage(self, html):
		html = etree.HTML(html)
		# 返回包含所有帖子链接的列表
		link_list = html.xpath(self.xpath_url)
		for link in link_list:
			link_url = self.baseUrl + link
			self.dealImage(self.loadRequest(link_url))

	def dealImage(self, html):
		html = etree.HTML(html)
		link_list = html.xpath(self.xpath_image)
		for link in link_list:
			print(link)
			self.writeImage(self.loadRequest(link), link[-10:])

	def writeImage(self, data, fileName):
		"""
			作用：写入磁盘
			html：响应内容
			filename：磁盘文件名
		"""
		# 写入磁盘文件
		with open("images/" + fileName, "w") as f:
			f.write(data)
		print("[LOG]：%s保存成功" % fileName)

	def tiebaSpider(self):
		"""
			作用：贴吧爬虫调度器，处理请求和响应
		"""
		for page in range(self.startPage, self.endPage + 1):
			pn = (page - 1) * 50
			# 转码后返回url编码的字符串
			keyword = {"kw": self.tiebaName, "pn" : pn}
			fullUrl = self.baseUrl + "/f?" + urllib.urlencode(keyword)
			html = self.loadRequest(fullUrl)
			self.dealPage(html)

def main():
	tiebaImage = TiebaImage()	
	tiebaImage.tiebaSpider()

if __name__ == "__main__":
	main()
