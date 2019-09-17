# -*- encoding: utf-8 -*-
# @Time : 2018/10/23/023 8:43
# @Author : 山那边的瘦子
# @Email : 690238539@qq.com
# @File : pictools.py
# @Software: PyCharm

from PIL import Image


class image_aspect():
    """
    图片分辨率修改
    """

    def __init__(self, image_file, aspect_width, aspect_height):
        self.img = Image.open(image_file)
        self.aspect_width = aspect_width
        self.aspect_height = aspect_height
        self.result_image = None

    def change_aspect_rate(self):
        img_width = self.img.size[0]
        img_height = self.img.size[1]

        if (img_width / img_height) > (self.aspect_width / self.aspect_height):
            rate = self.aspect_width / img_width
        else:
            rate = self.aspect_height / img_height

        rate = round(rate, 1)
        print(rate)
        self.img = self.img.resize((int(img_width * rate), int(img_height * rate)))
        return self

    def past_background(self):
        self.result_image = Image.new("RGB", [self.aspect_width, self.aspect_height], (0, 0, 0, 255))
        self.result_image.paste(self.img, (
            int((self.aspect_width - self.img.size[0]) / 2), int((self.aspect_height - self.img.size[1]) / 2)))
        return self

    def save_result(self, file_name):
        self.result_image.save(file_name)


if __name__ == "__main__":
    image_aspect(r'C:\Users\hungtongx\Desktop\AB.png', 128, 128). \
        change_aspect_rate(). \
        past_background(). \
        save_result(r'C:\Users\hungtongx\Desktop\AB.png')
