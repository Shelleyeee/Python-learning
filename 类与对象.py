# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

class dessert():
#定义一个甜点的类别
    sweet = True
    #属性“甜”为真
    def taste(self,people):
    #定义一个“品尝”的方法，参数有两个。其中self是系统预设关键词，代表的是这个对象本身，调用该方法时可省略这个参数的填写。
    #people是吃食物的人。
        print(people,'说：真好吃！')
        #输出people,'说：真好吃！'
milkytea = dessert()
cake = dessert()
cookies = dessert()
#定义dessert中的对象
print(type(milkytea))
#输出食物炸鸡的数据类型
print(cake.sweet)
#输出食物炸鸡的delicious属性
cookies.taste('周鹤阳')
#调用品尝的方法，吴枫吃掉炸鸡