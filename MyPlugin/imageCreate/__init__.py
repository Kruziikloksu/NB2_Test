from asyncio.windows_events import NULL
import math
from posixpath import split
import re
import configparser
from fileinput import close
from operator import le
from pickle import NONE
from socket import MsgFlag
import string
from tokenize import group
from nonebot import get_driver
from .config import Config
from configparser import ConfigParser   # Python2中是from ConfigParser import ConfigParser
import base64
import os
import random
import ast
from datetime import date
from nonebot.plugin import on_keyword, on_startswith, on_endswith, on_regex, on_message,on_notice
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot import on_message
from httpx import AsyncClient

from PIL import Image,ImageDraw,ImageFont
import cv2
import numpy as np



global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)





#封装测试
def cqAt(qqId):
    cqAtCode = f'[CQ:at,qq={qqId}]'
    return cqAtCode

def cqImg(imgPath):
    thisImgMsg=MessageSegment.image(f'file:///{imgPath}')
    return thisImgMsg

def RandomFileGet(firstdir):
    pathdir = os.listdir(firstdir)#获取所在路径下的所有文件
    path1 = pathdir[:-1]#剔除最下级
    path = []
    for path2 in path1:
        path.append(firstdir + path2)
    thisRandomFile=path[random.randint(0,len(path))]
    return thisRandomFile

def StrToBase64(strInput):
    #strInput="A319060267"
    bs=str(base64.b64encode(str(strInput).encode('utf-8')),"utf-8")
    return (bs)
    #print('解码：'+str(base64.b64decode(bs),"utf-8"))


#十六进制和字符串互相转换
def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])
#'utf-8'
def str_to_hex(s):
    return ' '.join([hex(ord(c)).replace('0x', '') for c in s])

def split_str(s):
    return list(s)



# 图片背景透明化
def transPNG(srcImageName):
    img = Image.open(srcImageName)
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = list()
    for item in datas:
        if item[0] > 220 and item[1] > 220 and item[2] > 220:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    return img


imgPath="C:/Users/Scedovah/Desktop/imgs/createdImg.png"
def addText(thisStr):
    global imgPath
    newImg = Image.new('RGBA',(600,400),'white')
    newImg.save(imgPath)
    font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 15)
    size = newImg.size
    width = size[0]
    high = size[1]
    lenth = len(thisStr)*3
    draw = ImageDraw.Draw(newImg)
    draw.text((width*1/8,high*1/8),thisStr,fill='black',font=font)
    #newImg.show()
    newImg.save(imgPath)

def imageAdd():
    global imgPath
    # 加载第一张图片
    im = Image.open('C:\\Users\\Scedovah\\Desktop\\imgs\\testpng.png')
    # 获取图片的长宽
    x, y = im.size
    #im.resize()#返回此图像的调整大小后的副本，按照等比例缩小为 x：1024，y：int(1024/x*y)👇
    im = im.resize((520,int(520/x*y)),Image.ANTIALIAS) # 对图片的大小进行调整
    # 参数解析：
    # (520,int(520/x*y) 对应需要调整的长和宽
    # 第二个参数Image.ANTIALIAS解析如下：
    # Image.NEAREST ：低质量
    # Image.BILINEAR：双线性
    # Image.BICUBIC ：三次样条插值
    # Image.ANTIALIAS：高质量
    #im.show() 
    # 如图👇
    # 同理加载第二张图片
    im2 = Image.open("C:\\Users\\Scedovah\\Desktop\\imgs\\test.jpg")
    # 获取图片的长宽
    x, y = im2.size
    #im2.resize()#返回此图像的调整大小后的副本，按照等比例缩小为 x：1024，y：int(1024/x*y)👇
    im2 = im2.resize((520,int(520/x*y)),Image.ANTIALIAS) # 对图片的大小进行调整
    #im2.show() 
    # 如图👇
    # 最后呢我们在创建一个长宽适合两张图片大小的图
    x0=im.size[0]
    y0=im.size[1]
    x1=im2.size[0]
    y1=im2.size[1]
    #image = Image.new('RGB', (520, int(520/x0*y0)+int(520/x1*y1)), (255,0,0))
    image = Image.new('RGB', (x0,y0), (255,0,0))
    image.paste(im2,(0,0)) 
    image.paste(im,(0,0),im)
    #image.paste(im2,(0,int(520/x0*y0)))
    # .paste复制粘贴的效果
    # 参数解析：
    # 第一个参数表示被粘贴的图片（im and img）
    # 第二次参数表示粘贴图片的定位点（每张的图左上角都为（0，0））可以用ps软件查看图片的坐标位置！
    #image.show()
    # 如图👇
    image.save('C:\\Users\\Scedovah\\Desktop\\imgs\\thisPNG.png')


def gifCreate():
    # 初始化图片地址文件夹途径
    image_path ="C:\\Users\\Scedovah\\Desktop\\wolves"
    # 获取文件列表
    files = os.listdir(image_path)
    # 定义第一个文件的全局路径
    file_first_path = os.path.join(image_path, files[0])
    # 获取Image对象
    img = Image.open(file_first_path)#.resize((520,520),Image.ANTIALIAS)
    bgImg = Image.new('RGBA',(1600,1600),'white')
    bgImg.paste(img.convert("RGBA")  ,(math.floor((bgImg.size[0]-img.size[0])/2),math.floor((bgImg.size[1]-img.size[1])/2)),img.convert("RGBA")  )
    # 初始化文件对象数组
    images = []
    for image in files[1:]:
        # 获取当前图片全量路径
        img_path = os.path.join(image_path, image)
        # 将当前图片使用Image对象打开、然后加入到images数组
        curImg=Image.open(img_path)
        newImg = Image.new('RGBA',(1600,1600),'white')
        newImg.paste(curImg.convert("RGBA")  ,(math.floor((newImg.size[0]-curImg.size[0])/2),math.floor((newImg.size[1]-curImg.size[1])/2)),curImg.convert("RGBA")  )
        images.append(newImg)#.resize((520,520),Image.ANTIALIAS))
    # 保存并生成gif动图
    bgImg.save('C:\\Users\\Scedovah\\Desktop\\imgs\\thisGIF.gif', save_all=True, append_images=images, loop=0, duration=200)

from PIL import Image, ImageSequence

def gifBreak():
    with Image.open("C:\\Users\\Scedovah\\Desktop\\Fight\\Fighting.gif") as im:
        index = 1
        for frame in ImageSequence.Iterator(im):
            frame.save(f"C:\\Users\\Scedovah\\Desktop\\Fight\\FightImg{index}.png")
            index += 1

#gifBreak()




imgAddText = on_startswith(['图片生成'],priority=50)# 创建消息匹配事件响应器
@imgAddText.handle()
async def imgAddText_handle(bot: Bot, event: Event):#异步定义
    thisText=event.get_plaintext()[4:]
    thisText=f'第一行文本\n'\
        f'图片路径:{imgPath}\n'\
        f'测试'
    addText(thisText)
    imageAdd()
    gifCreate()
    await imgAddText.send(MessageSegment.image(f'file:///C:\\Users\\Scedovah\\Desktop\\imgs\\thisGIF.gif'))
    await imgAddText.send(MessageSegment.image(f'file:///C:\\Users\\Scedovah\\Desktop\\imgs\\thisPNG.png'))
    await imgAddText.finish(MessageSegment.image(f'file:///{imgPath}'))


# def fightingCreate():
#     # 初始化图片地址文件夹途径
#     image_path ="C:\\Users\\Scedovah\\Desktop\\gif1"
#     # 获取文件列表
#     files = os.listdir(image_path)
#     # 定义第一个文件的全局路径
#     file_first_path = os.path.join(image_path, files[0])
#     # 获取Image对象
#     img = Image.open(file_first_path)#.resize((520,520),Image.ANTIALIAS)
#     #imgHead1 = Image.open('C:\\Users\\Scedovah\\Desktop\\Heads\\lje.png')
#     #img.paste(imgHead1,(150,50),imgHead1)
#     # 初始化文件对象数组
#     images = []
#     for image in files[1:]:
#         # 获取当前图片全量路径
#         img_path = os.path.join(image_path, image)
#         # 将当前图片使用Image对象打开、然后加入到images数组
#         curImg=Image.open(img_path)
#         #curImg.paste(imgHead1,(150,50),imgHead1)
#         images.append(curImg)
#     # 保存并生成gif动图
#     img.save('C:\\Users\\Scedovah\\Desktop\\testGIF.gif', save_all=True, append_images=images, loop=0, duration=165)

# fightingCreate()