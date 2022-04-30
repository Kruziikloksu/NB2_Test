from asyncio.windows_events import NULL
from email import message
from msvcrt import open_osfhandle
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
from nonebot.plugin import on_keyword, on_startswith, on_endswith, on_regex, on_message,on_notice,on_request,on_metaevent,on_command
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11 import Message, MessageSegment, GroupMessageEvent,MessageEvent,MetaEvent,RequestEvent,NotifyEvent,NoticeEvent,GroupRequestEvent,GroupDecreaseNoticeEvent,GroupIncreaseNoticeEvent,GroupAdminNoticeEvent,GroupBanNoticeEvent,GroupRecallNoticeEvent,GroupUploadNoticeEvent,LuckyKingNotifyEvent,FriendRecallNoticeEvent,FriendAddNoticeEvent,PrivateMessageEvent,LifecycleMetaEvent,FriendRequestEvent,PokeNotifyEvent,HonorNotifyEvent,HeartbeatMetaEvent

from nonebot import on_message
from httpx import AsyncClient
from nonebot.params import EventType , EventMessage,EventToMe,EventPlainText, EventParam

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from nonebot import get_bot
import requests


import datetime
 
# 获取今天（现在时间）
today = datetime.date.today()
print(today)
 


from nonebot import require
scheduler = require("nonebot_plugin_apscheduler").scheduler


botDir=os.path.abspath('.')
print(botDir)
url="https://www.bilibili.com/"
chrome_path=botDir+"\\MyPluginData\\chromedriver_win32\\chromedriver.exe"
screenshot_path=botDir+"\\MyPluginData\\timeline.png"

def urlShotter(url):
    global chrome_path
    global screenshot_path
    URL = url
    # 用selenium打开网页
    # 首先要下载 Chrome webdriver

    ch_options = Options()
    ch_options.add_argument("--kiosk")
    ch_options.add_argument('window-size=1920x1080')
    ch_options.add_argument('--disable-gpu')
    ch_options.add_argument('--hide-scrollbars')
    ch_options.add_argument("--disable-blink-features=AutomationControlled")
    ch_options.add_argument('--headless') 
    # 在启动浏览器时加入配置
    driver = webdriver.Chrome(executable_path=chrome_path, chrome_options=ch_options)
    driver.get(URL)
    print(driver.page_source)
    time.sleep(2)
    driver.save_screenshot(screenshot_path)


def GetDateMessage():
    global currentMsg
    url = "http://timor.tech/api/holiday/next"
    res = requests.get(url).json()
    res = res['holiday']
    nameOfHoliday=res['name']
    dateOfHoliday=res['date']
    daysBeforeHoliday=res['rest']
    thisMsg=f'今天是{today}\n最近的假期是{dateOfHoliday}的{nameOfHoliday}\n距离{nameOfHoliday}还有{daysBeforeHoliday}天！'
    return thisMsg


#封装测试
def cqAt(qqId):
    cqAtCode = f'[CQ:at,qq={qqId}]'
    return cqAtCode

def cqImg(imgPath):
    thisImgMsg=f'[CQ:image,file=file:///{imgPath},type=show,id=40004]'#MessageSegment.image(f'[CQ:image,file=file:///{imgPath},type=show,id=40004]')
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


getUrlScreenshot = on_startswith(['查看截图'],priority=50)# 创建消息关键词匹配事件响应器
@getUrlScreenshot.handle()
async def getUrlScreenshot_handle(bot: Bot, event: Event):#异步定义
    global screenshot_path
    #thisGroupId = event.get_session_id().split("_")[1]     
    urlShotter(url)
    time.sleep(3)
    await getUrlScreenshot.finish(MessageSegment.image(f'file:///{screenshot_path}'))
    #await getUrlScreenshot.finish(Message(f'[CQ:image,file={screenshot_path}]'))

getSixtySec = on_startswith(['今日新闻'],priority=50)# 创建消息关键词匹配事件响应器
@getSixtySec.handle()
async def getSixtySec_handle(bot: Bot, event: Event):#异步定义
    global screenshot_path
    await getSixtySec.finish(MessageSegment.image(f'https://api.03c3.cn/zb/'))




@scheduler.scheduled_job('cron', hour=8,minute=00)
async def sendMySixtySec():
    bot = get_bot('2546707335')
    global screenshot_path
    #result =  bot.send_private_msg(user_id=623985209,message=MessageSegment.image(f'https://api.03c3.cn/zb/'))
    await bot.send_private_msg(user_id=623985209,message=GetDateMessage())
    await bot.send_private_msg(user_id=623985209,message=MessageSegment.image(f'https://api.03c3.cn/zb/'))


#scheduler.add_job(run_every_day_from_program_start, "interval", days=1, id="xxx")
job = scheduler.add_job(sendMySixtySec, 'interval', days=1)
#job.remove()