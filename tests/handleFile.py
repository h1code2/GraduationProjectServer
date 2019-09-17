# -*- encoding: utf-8 -*-
# @Time : 2018/12/5/005 18:43
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : handleFile.py
# @Software: PyCharm


def markfunc(n):
	return lambda x: x + n


f = markfunc(24)

print(f(2))

a = [25, 454, 7879]

a.reverse()

print(a)

d = dict(hello='hello001')
e = dict(hello1='hello002')

for k, v in zip(d.items(), e.items()):
	print(k, v, end='+')

# print(d)
