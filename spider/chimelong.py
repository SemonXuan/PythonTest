# -*- coding:utf-8 -*-
import urllib2
import urllib

def loadPage(url):
	headers = {"User-Agent" : "Mozilla/4.0 (compatible; MISE 7.0; Windows NT 6.0; Trident/5.0)"}
	request = urllib2.Request(url, headers = headers)
	try:
		response = urllib2.urlopen(request)
	except:
		print("失败")
	with open("chimelong.html", "w") as f:
		f.write(response.read())

def main():
	id = raw_input("请输入id：")
	fromDate = raw_input("请输入起始时间：")
	endDate = raw_input("请输入终止时间：")

	url = "https://h.chimelong.com/" + id + "?" + urllib.urlencode({"date":fromDate, "edate":endDate})
	loadPage(url)

if __name__ == "__main__":
	main()
