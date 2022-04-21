from asyncio.windows_events import NULL
import re
import configparser
from fileinput import close
from operator import le
from pickle import NONE
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
from nonebot.params import EventType



global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)

# proDir = os.path.split(os.path.realpath(__file__))[0]
# # proDir = os.path.dirname(os.path.realpath(__file__))  与上面一行代码作用一样
# configPath = os.path.join(proDir, "WordDB.txt")
# path = os.path.abspath(configPath)

import json

dict_var = {
    'name': 'Cactus', 
    'age': 18, 
    'skills': ['Python', 'Java', 'Go', 'NodeJS'], 
    'has_blog': True, 
    'gf': None
}

print(json.dumps(dict_var))
print(json.dumps(dict_var, indent=2,sort_keys=True, ensure_ascii=False))







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

from nonebot import on_command
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.adapters import Message
from nonebot.params import Arg, CommandArg, ArgPlainText


