# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 19:22:22 2022

@author: 10740
"""

import requests,json
#引用requests模块
res = requests.get('https://www.zhihu.com/people/grass-40/followers?page=16')

#调用get方法，下载网页源代码
jsonres = json.loads(res.text)
list = jsonres['data']['hotkey']
for x in list:
    print(x['k'])



