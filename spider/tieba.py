# -*- coding: utf-8 -*-
import urllib
import urllib2

def loadPage(url, fileName):
	headers = {"User-Agent" : "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
	request = urllib2.Request(url, headers = headers)
	
	try:
		response = urllib2.urlopen(request)
		print("[LOG]：%s下载成功" % fileName)
		html = response.read()
		return html
	except RuntimeError, e:
		print(e.message)
		print("[ERR]：下载失败")

def writePage(html, fileName):
	with open(fileName, "w") as f:
		f.write(html)
	print("[LOG]：%s保存成功" % fileName)

def tiebaSpider(url, searchName, startPage, endPage):
	
	for page in range(startPage, endPage + 1):
		pn = (page - 1) * 50
        	keyword = {"kw": searchName, "pn" : pn}
		fullUrl = url + urllib.urlencode(keyword)
		fileName = searchName + str(page) + ".html"
	
		html = loadPage(fullUrl, fileName)
		writePage(html, fileName)

def main():
	tiebaName = raw_input("请输入贴吧名：")
	startPage = int(raw_input("请输入起始页："))
	endPage = int(raw_input("请输入终止页："))
	
	baseUrl = "https://tieba.baidu.com/f?"
	tiebaSpider(baseUrl, tiebaName, startPage, endPage)

if __name__ == "__main__":
	main()
