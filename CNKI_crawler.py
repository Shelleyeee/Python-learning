# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 15:00:06 2023

@author: 10740
"""

'''Resource https://www.jianshu.com/p/56722a33ad07'''


import time 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#可以对网页上元素是否存在，可点击等等进行判断，一般用于断言或与WebDriverWait配合使用。
#WebDriverWait中的until()和until_not()中的方法，必须是可调用的方法。
#原文链接：https://blog.csdn.net/kelanmomo/article/details/82886718
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from urllib.parse import urljoin

# #交互动作
# element = find_element_by_id('id')

# element.send_keys('Hello')  # 传入Hello
# element.clear()  # 清除输入框
# element.click()  # 点击元素
# element.text  # 获取元素文本信息
# element.get_attribute('href')  # 获取元素属性

#浏览器初始化
#get直接返回，不再等待界面加载完成
desired_capabilities = DesiredCapabilities.EDGE
desired_capabilities["pageLoadStrategy"] = "none"

# 设置edge驱动器的环境
options = webdriver.EdgeOptions()
# 设置chrome不加载图片，提高速度
options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
# 设置不显示窗口
#options.add_argument('--headless')
# 创建一个驱动器,打开知网
driver = webdriver.Edge(options=options)
driver.get('https://www.cnki.net/')
# 设置搜索主题
theme = "跨境资本流动"
# 设置所需篇数
papers_need = 21
##定位搜索框的XPATH（检查-左面点击搜索框，找到对应网页代码-右击复制-复制完整的XPATH）
#Xpath是用来确定XML文档中某处位置的语言
# input_xpath =  '/html/body/div[2]/div[2]/div/div[1]/input[1]'
# button_xpath =  '/html/body/div[2]/div[2]/div/div[1]/input[2]'
WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,'''//*[@id="txt_SearchText"]''') ) ).send_keys(theme)
# 点击搜索
WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[2]/div[2]/div/div[1]/input[2]") ) ).click()
time.sleep(3)

# 点击切换中文文献
WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[1]/div/div/div/a[1]") ) ).click()
time.sleep(1)

# # 按照被引量倒序排序
# WebDriverWait( driver, 200 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[1]/div[2]/div[3]/ul/li[3]") ) ).click()
# time.sleep(1)

# 获取总文献数和页数
res_unm = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located( (By.XPATH ,"/html/body/div[3]/div[2]/div[2]/div[2]/form/div/div[1]/div[1]/span[1]/em") ) ).text

# 去除千分位里的逗号
res_unm = int(res_unm.replace(",",''))
page_unm = int(res_unm/20) + 1
print(f"共找到 {res_unm} 条结果, {page_unm} 页。")

#创建csv文件用于保存
result = {'题目':[],
          '作者':[],
          '来源':[],
          '日期':[],
          '数据库':[],
          '作者单位':[],
          '摘要':[],
          '关键词':[],
          '链接':[]
          }

   
# 赋值序号, 控制爬取的文章数量
count = 1
# 当，爬取数量小于需求时，循环网页页码
while count < papers_need:
    # 等待加载完全，休眠3S
    time.sleep(2)
    #获得爬虫列表***
    title_list = WebDriverWait( driver, 10 ).until( EC.presence_of_all_elements_located( (By.CLASS_NAME  ,"fz14") ) )
    #判断定位的元素范围内，至少有一个元素存在于页面当中，存在则以list形式返回元素本身，不存在则报错
    
    # 循环网页一页中的条目
    for i in range(len(title_list)):

        try:
            term = count%20   # 本页的第几个条目
            title_xpath = "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr["+str(term)+"]/td[2]"
            author_xpath = "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr["+str(term)+"]/td[3]"
            source_xpath = "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr["+str(term)+"]/td[4]"
            date_xpath = "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr["+str(term)+"]/td[5]"
            database_xpath = "/html/body/div[3]/div[2]/div[2]/div[2]/form/div/table/tbody/tr["+str(term)+"]/td[6]"
                       
            title = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH ,title_xpath) ) ).text
            authors = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH,author_xpath) ) ).text
            source = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH ,source_xpath) ) ).text
            date = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH ,date_xpath) ) ).text
            database = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH,database_xpath) ) ).text
                        
            # 点击条目
            title_list[i].click()
            # 获取driver的句柄
            n = driver.window_handles 
            # driver切换至最新生产的页面
            driver.switch_to.window(n[-1])  
            # 开始获取页面信息
            # title = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,"/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h1") ) ).text
            # authors = WebDriverWait( driver, 10 ).until( EC.presence_of_element_located((By.XPATH ,"/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[1]") ) ).text
            institute = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.XPATH ,"/html/body/div[2]/div[1]/div[3]/div/div/div[3]/div/h3[2]") ) ).text
            abstract = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.CLASS_NAME  ,"abstract-text") ) ).text
            try:
                keywords = WebDriverWait( driver, 100 ).until( EC.presence_of_element_located((By.CLASS_NAME  ,"keywords") ) ).text[:-1]
            except:
                keywords = '无'
            url = driver.current_url
            # 获取下载链接 
            #link = WebDriverWait( driver, 10 ).until( EC.presence_of_all_elements_located((By.CLASS_NAME  ,"btn-dlpdf") ) )[0].get_attribute('href')
            #link = urljoin(driver.current_url, link)

            # 写入文件
            result["题目"].append(title)
            result["作者"].append(authors)
            result["来源"].append(source)
            result["日期"].append(date)
            result["数据库"].append(database)
            result["作者单位"].append(institute)
            result['摘要'].append(abstract)
            result["关键词"].append(keywords)
            result['链接'].append(url)
            
            df = pd.DataFrame(result)
            df.to_csv('C:/Users/10740/Desktop/cnki_paper.csv', encoding='gbk')
            

        except:
            print(f" 第{count} 条爬取失败\n")
            # 跳过本条，接着下一个
            
            continue
        finally:
            # 如果有多个窗口，关闭第二个窗口， 切换回主页
            n2 = driver.window_handles
            if len(n2) > 1:
                driver.close()
                driver.switch_to.window(n2[0])
            # 计数,判断需求是否足够
            count += 1
            if count > papers_need:
                exit()
    
    # 切换到下一页
    WebDriverWait( driver, 100 ).until( EC.presence_of_element_located( (By.XPATH ,"//a[@id='PageNext']") ) ).click()
    

# 关闭浏览器
driver.close()






