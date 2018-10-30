#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 18-10-22 上午10:20
# @Author  : Lone
# @Site    : 
# @File    : TestRunner.py
# @Software: PyCharm

import os.path
from labeltest.label_test import LabelTest

def test_runner():
    info_path = os.path.abspath(".")
    info_name = info_path + '/info.txt'
    print(info_name)
    info = []
    labelName = []
    with open(info_name, "r") as f:
        info = f.readlines()

    print(info)
    for i in range(2, len(info) - 1):
        labelName.append(info[i].rstrip())
    print(labelName)
    for i in labelName:
        labelTest = LabelTest(info[0].rstrip(), info[1].rstrip(), i)
        res = labelTest.getRes()
        print("测试标签 [" + i + "] 测试结果如下：")
        print("正确率 = %.4f\n召回率 = %.4f\nf1 = %.4f\n" % res)
        with open (info_path + "/log.txt", "a") as f:
            f.writelines("测试标签 [" + i + "] 测试结果如下：\n")
            f.writelines("正确率 = %.4f\n召回率 = %.4f\nf1 = %.4f\n" % res)


if __name__ == "__main__":
    test_runner()
