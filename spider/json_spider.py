# -*- coding:utf-8 -*-
import requests
import json
import jsonpath

# 可以处理磁盘文件交互，将文本编码格式按utf-8处理
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

class LagouSpider:
	def __init__(self):
		self.headers = {
			"Referer" : "https://www.lagou.com/jobs/list_python%E7%88%AC%E8%99%AB?labelWords=sug&fromSearch=true&suginput=python",
			"User-Agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
		}
		self.baseUrl = "https://www.lagou.com/jobs/positionAjax.json"
		self.positionName = raw_input("请输入需要抓取的职位名：")
		self.cityName = raw_input("请输入需要抓取的城市名：")
		self.endPage = int(raw_input("请输入需要抓取的页数："))
		self.page = 1
		self.flag = "false"

	def loadPage(self):
		params = {"city" : self.cityName,"needAddtionalResult" : "false"}
		formdata = {"first" : self.flag, "pn" : self.page, "kd" : self.positionName}
		try:
			print "[LOG]：正在处理第 %d 页..."% self.page
			response = requests.post(self.baseUrl, params = params, data = formdata, headers = self.headers)
		except Exception, e:
			print "[ERR]：请求处理失败..."
			print e
		jsonobj = response.json()
		
		"""
		# urllib2的用法
		params = urllib.urlencoded(params)
		data = urllib.urlencoded(formdata)
		url = self.baseUrl + params
		request = urllib2.Request(url, data = data, headers = self.headers)
		response = urllib2.urlopen(request)
		jsonobj = json.loads(response.read())
		"""

		result_list = jsonpath.jsonpath(jsonobj, "$..result")[0]
		item_list = []
		try:
			for result in result_list:
				item = {}
				item["城市"] = result['city'] if result['city'] else "NULL"
				item["公司名"] = result['companyFullName'] if result['companyFullName'] else "NULL"
				item["区域"] = result['district'] if result['district'] else "NULL"
				item["发布时间"] = result['createTime'] if result['createTime'] else "NULL"
				item["薪资"] = result['positionName'] if result['positionName'] else "NULL"
				item_list.append(item)
			return item_list
		except Exception, e:
			print "[ERR]：数据提取失败"
			print e
			return []

	def startWork(self):
		position_list = []
		while self.page <= self.endPage:
			if self.page == 1:
				self.flag = "true"
			else:
				self.flag = "false"
			item_list = self.loadPage()
			position_list += item_list
			self.page += 1
		content = json.dumps(position_list, ensure_ascii = False)
		with open("lagou_info.json", "w") as f:
			f.write(content)

def main():
	spider = LagouSpider()
	spider.startWork()

if __name__== "__main__":
	main()
