# -*- coding:utf-8 -*-
import datetime

from PIL import Image, ImageDraw, ImageFont
from math import sqrt
# 图片拼接
# import PIL.Image as Image
import os, sys


def tu_pj(num, model):
    if os.path.exists('./images/final'):
        print('exists')
    else:
        os.mkdir('./images/final')

    mw = 1000  # 图片大小+图片间隔
    ms = 5
    a = 1000
    if int(str(sqrt(num)).split('.')[1]) > 0 or int(str(sqrt(num)).split('.')[0]) == 1:
        frame = int(str(sqrt(num)).split('.')[0]) + 1
    else:
        frame = int(str(sqrt(num)).split('.')[0])
    print('frame:', frame)
    msize = a * frame

    fpre = "x"  # 图片前缀
    toImage = Image.new('RGB', (msize, msize))

    total = 0

    for y in range(1, frame + 1):  ## 先试一下 拼一个5*5 的图片
        for x in range(1, frame + 1):
            total += 1
            # 之前保存的图片是顺序命名的，x_1.jpg, x_2.jpg ...
            if total <= num:
                fname = "./images/fullNew/%s_%s.jpg" % (model, total)
                # fname = "./tu_/result_%s.jpg" % x
                # print('fname:', fname)
                try:
                    fromImage = Image.open(fname)
                except:
                    pass
                # fromImage =fromImage.resize((mw, mw), Image.ANTIALIAS)   # 先拼的图片不多，不用缩小
                try:
                    # toImage.paste(fromImage)
                    toImage.paste(fromImage, ((x - 1) * mw, (y - 1) * mw))
                # toImage.paste(fromImage, ((x - 1) * mw, (x - 1) * mw))
                except:
                    pass

    toImage.save('./images/final/%s.jpg' % model)

# 加文字水印


def add_num(image, newname, text):
    # num = 0
    if os.path.exists('./images/fullNew'):
        print('exists')
    else:
        os.mkdir('./images/fullNew')


    # draw = ImageDraw.Draw(img)
    # myfont = ImageFont.truetype('C:/windows/fonts/Arial.ttf', size=40)

    # image = Image.open('./tu/x_%s.jpg' % num)
    draw = ImageDraw.Draw(image)
    # myfont = ImageFont.truetype('/Library/Fonts/%s' % 'AdobeFangsongStd-Regular.otf', size=40)
    myfont = ImageFont.truetype('/Library/Fonts/%s' % 'Songti.ttc', size=40)
    # myfont = ImageFont.truetype('/Library/Fonts/%s' % 'AdobeHeitiStd-Regular.otf', size=40)
    # myfont = ImageFont.truetype('/Library/Fonts/%s' % 'AdobeKaitiStd-Regular.otf', size=40)
    # 黑色
    # fillcolor = "#000000"
    # 鲜绿色
    fillcolor = "#00FF00"
    # 粉红色
    # fillcolor = "#FF00FF"
    # 红色
    # fillcolor = "#FF0000"
    # 黄色
    # fillcolor = "#FFFF00"
    width, height = image.size
    draw.text((width / 2 - 130, height / 2 - 320), text, font=myfont, fill=fillcolor)
    image.save('./images/fullNew/%s' % newname)
    # num += 1

    # return 0
if __name__ == '__main__':
    num = 0
    # line_list = [line.strip() for line in open('ziti.txt') if line]
    # for line in line_list:
    image = Image.open('./images/full/Air9S_14.jpg')
    text = '''
        三洋官方旗舰店
        页面价: 3999    
    '''
    add_num(image, 'text.jpg', text)
    # print(line)
    num += 1
    # image.show()



