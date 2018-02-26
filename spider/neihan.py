# -*- coding:utf-8  -*-
import requests
import re

class DuanziSpider:
	def __init__(self):
		self.baseURL = "http://www.budejie.com/text/"
		self.headers = headers = {"User-Agent" : "Mozilla/4.0 (compatible; MISE 7.0; Windows NT 6.0; Trident/5.0)"}
		# 表示页码
		self.page = 1

		# 匹配每条段子的正则表达式
		# 默认.在单行中进行匹配（.不匹配换行符）
		# re.S表示进行全文匹配，开始DOTALL模式，.也可以匹配换行符
		# .* ：尽可能多的匹配
		# .*? ：尽可能少的匹配
		self.pattern_page = re.compile('<div class="j-r-list-c-desc">(.*?)</div>', re.S)

		# 处理段子里的无效字符
		# <(.*?)> 表示HTML实体字符，如<a>
		# \s 表示空白字符和换行符
		self.pattern_content = re.compile(r"<(.*?)>")

	def loadPage(self):
		"""
			发送每一页的请求，并提取所有的段子文本
		"""
		# 拼接每一页的url地址
		url = self.baseURL + str(self.page)
		# 发送每一页的请求，返回相应
		html = requests.get(url, headers = self.headers).content
		# 匹配页面里的所有段子文本数据
		contentList = self.pattern_page.findall(html)
		# 处理每一条段子
		self.writePage(contentList)
	
	def writePage(self, contentList):
		"""
			处理每一条段子，并写入到磁盘文件里
			contenList：每一页所有的段子列表
		"""
		with open("duanzi.txt", "a") as f:
			for content in contentList:
				# 处理每一条段子，去除误用字符部分
				partternContent = self.pattern_content.sub("", content)
				print(partternContent)
				# 写入磁盘文件
				f.write(partternContent)

	def duanziSpider(self):
		"""
			控制爬取的页数
		"""
		while True:
			command = raw_input("输入回车继续爬取...(输入Q则退出)")
			if command == "Q":
				break
			self.loadPage()
			self.page += 1
def main():
	spider = DuanziSpider()
	spider.duanziSpider()

if __name__ == "__main__":
	main()
