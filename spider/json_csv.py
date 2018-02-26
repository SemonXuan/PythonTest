# -*- coding:utf-8 -*-

# csv处理模块
import csv
# json处理模块
import json

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

jsonFile = file("lagou_info.json", "r")
content_list = json.load(jsonFile)

csvFile = file("lagou_zhaopin.csv", "w")
csvWriter = csv.writer(csvFile)

sheet = content_list[0].keys()

# data = []
# for content in content_list:
#	data.append(content.values())

data = [content.values() for content in content_list]

csvWriter.writerow(sheet)
csvWriter.writerows(data)

csvFile.close()
jsonFile.close()
