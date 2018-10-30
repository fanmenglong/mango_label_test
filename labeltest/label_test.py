#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-10-22 上午9:57
# @Author  : Lone
# @Site    : 
# @File    : label_test.py
# @Software: PyCharm

import requests
import os.path
import urllib.parse

#print(os.path.abspath("."))

class LabelTest(object):
    def __init__(self, token, url, labelName):
        self.headers = {"Authorization": "Token " + token}
        self.url = url
        self.cntA = 0
        self.cntB = 0
        self.cntC = 0
        self.labelName = labelName

    def getParams(self):
        query = urllib.parse.urlparse(self.url).query
        return dict([(k, v[0]) for k, v in urllib.parse.parse_qs(query).items()])

    def getRightCnt(self):
        r = requests.get(self.url, headers=self.headers)
        print(r.status_code)
        res = r.json()
        print(res)
        r.close()
        #print(res)
        while True:
            for i in res["results"]:
                #print("-------------------------")
                if i["update_tag_ct"] == 0:
                    #print("----------正确的标签")
                    if i["cust_tag"] == self.labelName:
                        print("----------正确的[" + self.labelName + "]标签")
                        self.cntA += 1
            if not res["next"]:
                break
            r = requests.get(res["next"], headers=self.headers)
            res = r.json()
            r.close()

    def getWrongCnt(self):
        params = {}
        dictParams = self.getParams()
        print(dictParams)
        if "flow_id" in dictParams:
            params["flow_id"] = dictParams["flow_id"]
        if "start_date" in dictParams:
            params["start_date"] = dictParams["start_date"]
        if "end_date" in dictParams:
            params["end_date"] = dictParams["end_date"]
        if "task_id" in dictParams:
            params["task_id"] = dictParams["task_id"]
        if "hd_ct" in dictParams:
            params["hd_ct"] = dictParams["hd_ct"]
        url = urllib.parse.urlparse(self.url).scheme + "://" + urllib.parse.urlparse(self.url).netloc + "/api/task/call/update/tag/list/"
        print(url)
        r = requests.get(url, headers=self.headers, params=params)
        print(r.url)
        res = r.json()
        # r.close()
        print(r.status_code)
        print(res)
        for i in res["result"]:
            #print("----------错误的标签")
            if i["his_cust_tag"][0] == self.labelName:  # BUG 应该改为初始值 i["初始值"] == label
                print("----------错误的[" + self.labelName + "]标签")
                self.cntB += 1
            if i["cust_tag"] == self.labelName:
                print("----------应该为[" + self.labelName + "]标签")
                self.cntC += 1

    def getRes(self):
        self.getRightCnt()
        self.getWrongCnt()
        print("正确的标签数%d" % self.cntA)
        print("错误的标签数%d" % self.cntB)
        print("没打上标签数%d" % self.cntC)
        info_path = os.path.abspath(".")
        with open (info_path + "/log.txt", "a") as f:
            f.writelines("正确的标签数%d\n" % self.cntA)
            f.writelines("错误的标签数%d\n" % self.cntB)
            f.writelines("没打上标签数%d\n" % self.cntC)
        if self.cntA == 0:
            # print("测试标签 [" + self.labelName + "] 测试结果如下：")
            # print("正确率 = 0\n召回率 = 0\nf1 =0\n")
            return 0, 0, 0
        precisionRate = self.cntA / (self.cntA + self.cntB)
        recallRate = self.cntA / (self.cntA + self.cntC)
        # 正确率 * 召回率 * 2 / (正确率 + 召回率)
        f = precisionRate * recallRate * 2 / (precisionRate + recallRate)
        # print("测试标签 [" + i + "] 测试结果如下：")
        # print("正确率 = %.4f\n召回率 = %.4f\nf1 = %.4f\n" % precisionRate, recallRate, f)
        return precisionRate, recallRate, f


