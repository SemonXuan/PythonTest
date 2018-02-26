# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import json


class Tencent:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Trident/5.0)"}
        self.baseUrl = "https://hr.tencent.com/"
        self.startPage = int(raw_input("请输入起始页："))
        self.endPage = int(raw_input("请输入终止页："))

    def loadPage(self, url):
        html = requests.get(url, headers=self.headers).content
        soup = BeautifulSoup(html, "lxml")
        # lxml查找方法
        # //*[@class='even'] | //*[@class='odd']
        # select查找方法
        # soup.select(".even, .odd")
        # BeautifulSoup取出当前页面所有class为even和odd的标签节点，返回列表
        node_list = soup.find_all(class_=['even', 'odd'])
        self.dealNode(node_list)

    def dealNode(self, node_list):
        # 存储所有的职位信息列表
        item_list = []
        for node in node_list:
            item = {}
            item["position_name"] = node.select("td")[0].get_text()
            item["position_url"] = self.baseUrl + node.select("td a")[0].get("href")
            item["position_category"] = node.select("td")[1].get_text()
            item["position_num"] = node.select("td")[2].get_text()
            item["position_location"] = node.select("td")[3].get_text()
            item["postion_date"] = node.select("td")[4].get_text()
            item_list.append(item)
        # 把python格式的数据转换成json格式的字符串
        # ensure_ascii = Fasle 表示如果items里有中文的话，禁用ascii编码处理
        content = json.dumps(item_list, ensure_ascii = False)
        with open("tencentHr.txt", "w") as f:
            f.write(content.encode("utf-8"))
        print("保存成功")

    def getTencent(self):
        for page in (self.startPage, self.endPage + 1):
            url = self.baseUrl + "position.php?&start=" + str((self.startPage - 1) * 10)
            self.loadPage(url)


def main():
    tencent = Tencent()
    tencent.getTencent()


if __name__ == "__main__":
    main()
