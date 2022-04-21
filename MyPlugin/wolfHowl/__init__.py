from asyncio.windows_events import NULL
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

def str_to_oo(s):
    return oct(ord(s))
def oo_to_str(s):
    return chr(int(s, 8))
def longStrTran(s):
    return ' '.join([str_to_oo(c) for c in s])
def longOoTran(s):
    return ''.join( [oo_to_str(b) for b in s.split(' ')])
def mathToWolf(s):
    return ''.join([c.replace('o','！').replace('0', '嗷').replace('1', '呜').replace('2', '呼').replace('3', '噜').replace('4', '嘟').replace('5', '咕').replace('6', '啾').replace('7', '咪').replace(' ', '汪') for c in s])
def wolfToMath(s):
    return ''.join([c.replace('！','o').replace('嗷', '0').replace('呜', '1').replace('呼', '2').replace('噜', '3').replace('嘟', '4').replace('咕', '5').replace('啾', '6').replace('咪', '7').replace('汪', ' ') for c in s])

def wolvesHowl(s):
    return mathToWolf(' '.join([str(oct(ord(c))).replace('0o','') for c in s]))
def unWolvesHowl(s):
    return longOoTran(''.join([wolfToMath(('嗷！'+c)) for c in str(s).split(' ')] ))




#=================================================================================
wolfHowl = on_startswith(['狼叫'],priority=50)# 创建消息匹配事件响应器
@wolfHowl.handle()
async def wolfHowl_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())#.extract_plain_text()
    thisMsgStr=thisMsgStr[2:]
    encodeMsg = longStrTran(thisMsgStr)
    woflMsg = mathToWolf(encodeMsg)
    #await wolfHowl.send(Message(encodeMsg))
    await wolfHowl.finish(Message(wolvesHowl(thisMsgStr)))
    #await wolfHowl.finish(Message(woflMsg))


unHowl = on_startswith(['翻译狼叫'],priority=50)# 创建消息匹配事件响应器
@unHowl.handle()
async def unHowl_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())#.extract_plain_text()
    thisMsgStr=thisMsgStr[4:]
    mathMsg = wolfToMath(thisMsgStr)
    decodeMsg = longOoTran(mathMsg)
    await unHowl.finish(Message(unWolvesHowl(thisMsgStr)))
    #await unHowl.finish(Message(decodeMsg))

# wolfHowl = on_startswith(['狼叫'],priority=50)# 创建消息匹配事件响应器
# @wolfHowl.handle()
# async def wolfHowl_handle(bot: Bot, event: Event):#异步定义
#     thisMsgStr=str(event.get_message())#.extract_plain_text()
#     thisMsgStr=thisMsgStr[2:]
#     encodeMsg = longStrTran(thisMsgStr)
#     woflMsg = mathToWolf(encodeMsg)
#     #await wolfHowl.send(Message(encodeMsg))
#     await wolfHowl.finish(Message(wolvesHowl(thisMsgStr)))
#     #await wolfHowl.finish(Message(woflMsg))

#msgTest=on_message(priority=51)
#@msgTest.handle()
#async def msgTest_handle(bot: Bot, event: Event):
#    thisMsgStr=str(event.get_message())#.extract_plain_text()
#    await msgTest.finish(thisMsgStr)