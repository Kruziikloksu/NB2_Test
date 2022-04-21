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
from turtle import onkey
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
from httpx import AsyncClient
from nonebot.internal.matcher import Matcher
from nonebot.params import EventType , EventMessage,EventToMe,EventPlainText, EventParam

global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)


masterQQ='623985209'
banTagList=['禁言我']

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

def LuckyStr(num):
    if num < 5:
        return '...下下签？'
    elif num < 15:
        return '下平签。'
    elif num < 25:
        return '下吉签。'
    elif num < 35:
        return '中下签。'
    elif num < 50:
        return '中平签。'
    elif num < 75:
        return '中吉签。'
    elif num < 85:
        return '大吉签！'
    elif num < 95:
        return '上吉签！！'
    else:
        return '上上签！！！'
    


#小玩具==========================================================================
randomFileChoose = on_keyword(['随机图片'],priority=50)# 创建消息关键词匹配事件响应器
@randomFileChoose.handle()
async def randomFileChoose_handle(bot: Bot, event: Event):#异步定义
    randomImagePath=str(RandomFileGet('C:/Users/Scedovah/Desktop/wolves/'))
    await randomFileChoose.finish(Message(cqImg(randomImagePath)))

jrrp = on_startswith(['每日一抽'],priority=50)# 创建消息关键词匹配事件响应器
@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):#异步定义
    rnd = random.Random()
    rnd.seed(StrToBase64(int(date.today().strftime("%y%m%d")) + int(event.get_user_id())))
    lucknum = rnd.randint(1,100)
    await jrrp.send(Message(f'[CQ:at,qq={event.get_user_id()}]今天抽到了...{LuckyStr(lucknum)}({lucknum}/100)'))
    await jrrp.finish(Message(f'[CQ:poke,qq={event.get_user_id()}]'))

getImage = on_keyword(['图片测试'],priority=50)
@getImage.handle()
async def getImage_handle(bot: Bot, event: Event):#异步定义
    randomNum=random.randint(0,100)
    msg1 = Message('看图')
    msg2 = MessageSegment.image('file:///C:/Users/Scedovah/Desktop/avatar.jpg')
    msg  = msg1 + msg2
    await getImage.finish(Message(f'{msg}'))


#群数据api测试==============================================================
thisGroupInfo = on_startswith("本群信息",priority=50)
@thisGroupInfo.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    thisGroupId = event.get_session_id().split("_")[1]
    # call_api的写法一
    groupData = await bot.call_api('get_group_info',**{
        'group_id' : thisGroupId
    })
    # 对json进行转义
    dataGI = ast.literal_eval(str(groupData))
    msg = f"\
群号：{dataGI['group_id']}\n\
群名称：{dataGI['group_name']}\n\
成员数：{dataGI['member_count']}"   
    await thisGroupInfo.finish(msg)

thisGroupMemberInfo = on_startswith("我的群信息",priority=50)
@thisGroupMemberInfo.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    thisGroupId = event.get_session_id().split("_")[1]
    thisGroupId = event.get_session_id().split("_")[1]
    groupMemberData = await bot.call_api('get_group_member_info',**{
        'group_id' : thisGroupId,
        'user_id'  : event.get_user_id()
    })
    dataGM = ast.literal_eval(str(groupMemberData))
    msg = f"\
QQ号：{dataGM['user_id']}\n\
昵称：{dataGM['nickname']}\n\
群名片：{dataGM['card']}\n\
入群时间：{dataGM['join_time']}\n\
等级：{dataGM['level']}"   
    await thisGroupMemberInfo.finish(msg)
#禁言========================================================
banMan = on_startswith("杀",priority=50)
@banMan.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    thisGroupId = event.get_session_id().split("_")[1]
    thisMsgStr=str(event.get_message()).replace(' ','')
    thisMsgStr=thisMsgStr[1:]
    banInfo=str(thisMsgStr[10:]).split(']')[0]
    banInfo2=thisMsgStr.split(']')[1].replace(' ','')
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id' : banInfo,
        'duration':  int(banInfo2)*60
    })

banMe = on_startswith("杀我",priority=50)
@banMe.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    thisGroupId = event.get_session_id().split("_")[1]
    thisMsgStr=str(event.get_message()).replace(' ','')
    thisMsgStr=thisMsgStr[2:]
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id' : event.get_user_id(),
        'duration':  int(thisMsgStr)*60
    })

banTag = on_keyword(banTagList,priority=50)
@banTag.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    thisGroupId = event.get_session_id().split("_")[1]
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id'  : event.get_user_id(),
        'duration' : 300
    })


#解除禁言====================================================
saveMan = on_startswith("解禁",priority=50)
@saveMan.handle()
async def _(bot: Bot, event: Event):
    thisGroupId = event.get_session_id().split("_")[1]
    thisMsgStr=str(event.get_message()).replace(' ','')
    thisMsgStr=thisMsgStr[1:]
    banInfo=str(thisMsgStr[10:]).split(']')[0]
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id' : banInfo,
        'duration': 0
    })
#转告主人====================================================
#/send_msg
askMe = on_startswith("转告主人",priority=50)
@askMe.handle()
async def _(bot: Bot, event: Event):
    thisMsg=event.get_event_description()
    await bot.call_api('send_msg',**{
    'message_type' : 'private',
        'user_id' : masterQQ,
        'message': thisMsg
    })
#get_forward_msg

 


