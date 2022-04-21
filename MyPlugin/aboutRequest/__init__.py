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


weather = on_command("weather", rule=to_me(), aliases={"天气", "天气预报"}, priority=5)




@weather.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    plain_text = args.extract_plain_text()  # 首次发送命令时跟随的参数，例：/天气 上海，则args为上海
    if plain_text:
        matcher.set_arg("city", args)  # 如果用户发送了参数 直接赋值




@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(city: Message = Arg(), city_name: str = ArgPlainText("city")):
    if city_name not in ["北京", "上海"]:  # 如果参数不符合要求，则提示用户重新输入
        # 可以使用平台的 Message 类直接构造模板消息
        await weather.reject(city.template("你想查询的城市 {city} 暂不支持，请重新输入！"))


    city_weather = await get_weather(city_name)
    await weather.finish(city_weather)




# 在这里编写获取天气信息的函数
async def get_weather(city: str) -> str:
    return f"{city}的天气是..."
