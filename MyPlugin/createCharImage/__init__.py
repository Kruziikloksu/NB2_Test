from asyncio.windows_events import NULL
from dataclasses import replace
from email import message
from msvcrt import open_osfhandle
import re
import configparser
from fileinput import close
from operator import le
from pickle import NONE
import string
from textwrap import fill
from tokenize import group
from turtle import width
from nonebot import get_driver
from .config import Config
from configparser import ConfigParser   # Python2中是from ConfigParser import ConfigParser
import base64
import os
import random
import ast
from datetime import date
from nonebot.plugin import on_keyword, on_startswith, on_endswith, on_regex, on_message,on_notice,on_request,on_metaevent,on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent,MessageEvent,MetaEvent,RequestEvent,NotifyEvent,NoticeEvent,GroupRequestEvent,GroupDecreaseNoticeEvent,GroupIncreaseNoticeEvent,GroupAdminNoticeEvent,GroupBanNoticeEvent,GroupRecallNoticeEvent,GroupUploadNoticeEvent,LuckyKingNotifyEvent,FriendRecallNoticeEvent,FriendAddNoticeEvent,PrivateMessageEvent,LifecycleMetaEvent,FriendRequestEvent,PokeNotifyEvent,HonorNotifyEvent,HeartbeatMetaEvent
from nonebot import on_message
from httpx import AsyncClient
from nonebot.params import EventType , EventMessage,EventToMe,EventPlainText, EventParam
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText
import requests
import time

global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)

from nonebot import get_bot

import cv2
import random
import numpy as np
from PIL import Image,ImageDraw,ImageFont, ImageEnhance

strImgMode='1'
botDir=os.path.abspath('.')
image_path=botDir+"\\MyPluginData\\StringImage\\downloadedImage\\"#.jpg"
charImage_path=botDir+"\\MyPluginData\\StringImage\\charImage\\"#.jpg"
charImage_path2=botDir+"\\MyPluginData\\StringImage\\charImage2\\"#2.jpg"
charImage_path3=botDir+"\\MyPluginData\\StringImage\\charImage3\\"#3.jpg"
charTxt_path=botDir+"\\MyPluginData\\StringImage\\charCreate.txt"


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



def img2strimg(frame, K=5 ):
    """
    利用 聚类 将像素信息聚为3或5类，颜色最深的一类用数字密集地表示，阴影的一类用“-”横杠表示，明亮部分空白表示。
    ---------------------------------
    frame：需要传入的图片信息。可以是opencv的cv2.imread()得到的数组，也可以是Pillow的Image.read()。
    K：聚类数量，推荐的K为3或5。根据经验，3或5时可以较为优秀地处理很多图像了。若默认的K=5无法很好地表现原图，请修改为3进行尝试。若依然无法很好地表现原图，请换图尝试。 （ -_-|| ）    
    ---------------------------------
    聚类数目理论可以取大于等于3的任意整数。但水平有限，无法自动判断当生成的字符画可以更好地表现原图细节时，“黑暗”、“阴影”、”明亮“之间边界在哪。所以说由于无法有效利用更大的聚类数量，那么便先简单地限制聚类数目为3和5。
    """
    if type(frame) != np.ndarray:
        frame = np.array(frame)

    height, width, *_ = frame.shape  # 有时返回两个值，有时三个值
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_array = np.float32(frame_gray.reshape(-1))

    # 设置相关参数。
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    flags = cv2.KMEANS_RANDOM_CENTERS
    # 得到labels(类别)、centroids(矩心)。
    # 如第一行6个像素labels=[0,2,2,1,2,0],则意味着6个像素分别对应着 第1个矩心、第3个矩心、第3、2、3、1个矩心。
    compactness, labels, centroids = cv2.kmeans(frame_array, K, None, criteria, 10, flags)
    centroids = np.uint8(centroids)

    # labels的数个矩心以随机顺序排列，所以需要简单处理矩心.
    centroids = centroids.flatten()
    centroids_sorted = sorted(centroids)
    # 获得不同centroids的明暗程度，0最暗
    centroids_index = np.array([centroids_sorted.index(value) for value in centroids])

    bright = [abs((3 * i - 2 * K) / (3 * K)) for i in range(1, 1 + K)]
    bright_bound = bright.index(np.min(bright))
    shadow = [abs((3 * i - K) / (3 * K)) for i in range(1, 1 + K)]
    shadow_bound = shadow.index(np.min(shadow))

    labels = labels.flatten()
    # 将labels转变为实际的明暗程度列表，0最暗。
    labels = centroids_index[labels]
    # 列表解析，每2*2个像素挑选出一个，组成（height*width*灰）数组。
    labels_picked = [labels[rows * width:(rows + 1) * width:2] for rows in range(0, height, 2)]

    canvas = np.zeros((3 * height, 3 * width, 3), np.uint8)
    canvas.fill(255)  # 创建长宽为原图三倍的白色画布。

    # 因为 字体大小为0.45时，每个数字占6*6个像素，而白底画布为原图三倍
    # 所以 需要原图中每2*2个像素中挑取一个，在白底画布中由6*6像素大小的数字表示这个像素信息。
    y = 8
    for rows in labels_picked:
        x = 0
        for cols in rows:
            if cols <= shadow_bound:
                cv2.putText(canvas, str(random.randint(2, 9)),
                            (x, y), cv2.FONT_HERSHEY_PLAIN, 0.45, 1)
            elif cols <= bright_bound:
                cv2.putText(canvas, "-", (x, y),
                            cv2.FONT_HERSHEY_PLAIN, 0.4, 0, 1)
            x += 6
        y += 6

    return canvas

def anoStrImg(thisUserId):
    img = cv2.imread(image_path+thisUserId+'.jpg')
    # 若字符画结果不好，可以尝试更改K为3。若依然无法很好地表现原图，请换图尝试。 -_-||
    str_img = img2strimg(img,3)
    cv2.imwrite(charImage_path+thisUserId+'.jpg', str_img)


def reduce_intensity_levels(img, level,thisUserId):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.copyTo(img, None)
    for x in range(img.shape[0]):
        for y in range(img.shape[1]):
            si = img[x, y]
            ni = int(level * si / 255 + 0.5) * (255 / level)
            img[x, y] = ni
    cv2.imwrite(charImage_path3+thisUserId+".jpg", img)
    return img


def transform(image_file,thisUserId):
    reduce_intensity_levels(cv2.imread(image_path+thisUserId+".jpg"), 16,thisUserId)
    codeLib = '@%#######<|*^"+==----         '
    count = len(codeLib)
    codePic = ''
    for h in range(0,image_file.size[1]):  #图片分辨率
        for w in range(0,image_file.size[0]):
            gray = image_file.getpixel((w,h)) #返回指定位置的像素
            codePic = codePic +''+ codeLib[int(((count-1)*gray)/256)]#建立灰度与字符集的映射
        codePic = codePic+'\r\n'
    randCodePic=''
    for num in codePic:
        randCodePic+=num
    return randCodePic

def addText(thisStr,image_file,thisUserId):
    global charImage_path2
    newImg = Image.new('RGB',(image_file.size[0]*6,image_file.size[1]*6),'white')
    newImg.save(charImage_path2+thisUserId+'.jpg')
    size = newImg.size
    draw = ImageDraw.Draw(newImg)
    draw.text((0,0),thisStr,fill='black',spacing=-5)
    #newImg.show()
    newImg.save(charImage_path2+thisUserId+'.jpg')


def strImgCreate(thisUserId):
    reduce_intensity_levels(cv2.imread(image_path+thisUserId+".jpg"), 16,thisUserId)
    image_file = Image.open(charImage_path3+thisUserId+'.jpg')
    image_file=image_file.resize((int(image_file.size[0]/3), int(image_file.size[1]/3)))#调整图片大小
    charCode=transform(image_file,thisUserId)
    addText(charCode,image_file,thisUserId)

    tmp = open(charTxt_path,'w')
    tmp.write(charCode)
    tmp.close()

#strImgCreate()

downloadImg = on_startswith("生成字符画",priority=50)
@downloadImg.handle()
async def _(bot: Bot, event: Event):
    global strImgMode
    thisMsgStr=str(event.get_message())
    thisUserId=event.get_user_id()
    print(thisMsgStr)
    fileUrl=(thisMsgStr.split('url=')[1]).split(']')[0]
    print('地址'+fileUrl) 
    url = fileUrl
    await requests_download(url,thisUserId+".jpg")
    #await downloadImg.send(requests_download(url,thisUserId+".jpg"))
    if strImgMode == '0':
        anoStrImg(thisUserId)
        await downloadImg.finish(MessageSegment.image(f'file:///{charImage_path}{thisUserId}.jpg'))
    if strImgMode == '1':
        strImgCreate(thisUserId)
        await downloadImg.finish(MessageSegment.image(f'file:///{charImage_path2}{thisUserId}.jpg'))

#[CQ:image,file=286c616e6b7e0152329b8776659cf584.image] [CQ:image,file=cd52b29ea1bc2cf64cd513823052f43a.image] 
async def requests_download(url,thisFileName):
    r =  requests.get(url)
    # 判断响应状态
    if r.status_code == 200:
        # 创建文件保存图片
        with open(image_path+thisFileName,'wb') as f:
            # 将图片字节码写入创建的文件中
            f.write(r.content)    
    else:
        print( '图片获取失败！危')

