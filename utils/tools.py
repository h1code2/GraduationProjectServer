# -*- encoding: utf-8 -*-
# @Time : 2018/10/17 20:13
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : tools.py
# @Software: PyCharm

import random
from utils import redis
from PIL import Image


def random_str(number):
    """
    生成number位数字字符串
    """
    r_code = ""
    for i in range(number):
        ch = chr(random.randrange(ord('0'), ord('9') + 1))
        r_code += ch
    return r_code


def img_to_arr(filePath):
    """
    图片文件转十六进制
    :param filePath:
    :return: 十六进制..
    """
    img = Image.open(filePath)
    out = ""
    width, height = img.size
    # width = 128
    # height = 128
    for y in range(0, height):
        for x in range(0, width):
            r, g, b = img.getpixel((x, y))
            # 8bit convert to 5bit
            px = hex((r >> 3) << 11 | (g >> 2) << 5 | b >> 3)
            # h = "变量1" if a > b else "变量2"
            pxx = str(px)[2:4]
            pxxx = pxx if len(pxx) == 2 else pxx + '0'
            out += pxxx + pxxx
    return out


def per_transform(per):
    """
    用户权限转换
    :param per:
    :return:
    """
    if per == 1:
        return '普通用户'
    elif per == 3:
        return '管理员'
    elif per == 15:
        return '超级管理员'
    elif per == 255:
        return "开发者"
    else:
        return '游客'
