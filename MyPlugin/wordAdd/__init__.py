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

global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)

# proDir = os.path.split(os.path.realpath(__file__))[0]
# # proDir = os.path.dirname(os.path.realpath(__file__))  与上面一行代码作用一样
# configPath = os.path.join(proDir, "WordDB.txt")
# path = os.path.abspath(configPath)
ini_absolute_path = 'C:/Users/Scedovah/Desktop/WDB/WordDB.txt'

def AddWord(groupId,targetWord,newContent)->str:
    targetWord=str(targetWord).replace('[cq','[CQ')
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(open(ini_absolute_path,encoding='utf-8'))  #指定encoding='utf-8'
    conf.add_section(groupId)#添加section
    if not conf.has_section(groupId) :
        conf.add_section(groupId)#添加section
        o=open(ini_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
    conf.clear
    conf.read(ini_absolute_path,encoding='utf-8')  
    if  conf.has_option(groupId, targetWord) :
        wordList=GetWord(groupId,targetWord)
        if not newContent in wordList :
            conf.read(ini_absolute_path,encoding='utf-8')
            thisContent= conf.get(groupId, targetWord)
            conf.set(groupId,targetWord,f'{thisContent}&Nex&{newContent}')
            o=open(ini_absolute_path, "w",encoding='utf-8') 
            conf.write(o)
            o.close()
            return f'添加成功！'
        else:
            return '该记录已存在，请勿重复添加！'
    conf.clear
    conf.read(ini_absolute_path,encoding='utf-8')  
    if  not  conf.has_option(groupId, targetWord) :
        conf.set(groupId,targetWord,newContent)
        thisContent= conf.get(groupId, targetWord)
        o=open(ini_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
        return f'添加成功！'

def GetWord(groupId,targetWord)->str:
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 指定encoding='utf-8'
    #targetWord=targetWord.replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('CQ','cq').replace.replace(':','$mh;')

    # thisContent= conf.get(groupId, targetWord)
    # contentList=thisContent.replace('&Nex&','\n')
    # return contentList

    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                thisContent= conf.get(groupId, targetWord)
                contentList=thisContent.replace('&Nex&','\n')
                return contentList
            else:
                return f'词条{targetWord}不存在！'
    else:
        return f'词条{targetWord}不存在！'

def GetRanWord(groupId,targetWord) ->str:
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    targetWord=targetWord
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                    thisContent= conf.get(groupId, targetWord)
                    contentList=thisContent.split('&Nex&')
                    return contentList[random.randint(0,len(contentList)-1)]
    else:
        return

def DelWord(groupId,targetWord)->str:
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                    conf.remove_option(groupId, targetWord) #删除指定section的key
                    o=open(ini_absolute_path, "w",encoding='utf-8') 
                    conf.write(o)
                    o.close()
                    return '删除成功！'
            return '未找到该词条！'
    return '未找到该词条！'





saveWord = on_startswith(['添加词条%'],priority=50)# 创建消息关键词匹配事件响应器
@saveWord.handle()
async def saveWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=thisWholeContent[0]
    thisContent=thisWholeContent[1]
    thisWord=(thisWord).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace(':','$mh;')#.replace('CQ','cq')#.replace('cq:','cq = ')
    #thisContent=repr(thisContent)
    thisGroupId = event.get_session_id().split("_")[1]       
    #await saveWord.send(Message(f'添加的文本是 {thisWord}')) 
    #await saveWord.send(Message(f'添加的内容是 {thisContent}')) 
    await saveWord.finish(Message(f'{cqAt(event.get_user_id())}{AddWord(thisGroupId,thisWord,thisContent)}'))

readWord = on_startswith(['查看词条%'],priority=50)# 创建消息关键词匹配事件响应器
@readWord.handle()
async def readWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=(thisWholeContent[0]).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('CQ','cq').replace(':','$mh;')#.replace('cq:','cq = ')
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    #await readWord.send(f'正在查询词条{thisWord}...')
    await readWord.finish(Message(GetWord(thisGroupId,thisWord)))

delWord = on_startswith(['删除词条%'],priority=50)# 创建消息关键词匹配事件响应器
@delWord.handle()
async def delWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=(thisWholeContent[0]).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('CQ','cq').replace(':','$mh;')#.replace('cq:','cq = ')
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    await delWord.finish(Message(DelWord(thisGroupId,thisWord)))

#root_dir=os.path.dirname(os.path.pardir('.')) 

readRanWord = on_message(priority=51,block=False)# 创建消息关键词匹配事件响应器
@readRanWord.handle()
async def readRanWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #eventContent=str(event)
    #await saveWord.send(Message(f'event是 {eventContent}'))  
    #thisMsgStr=event.get_message().extract_plain_text()
    #thisWholeContent=str(thisMsgStr).split('#')
    thisWord=(thisMsgStr).replace('[','$91;').replace(']','$93;').replace('CQ','cq').replace('=','$eql;').replace(':','$mh;')#.replace('cq:','cq = ')
    #thisWholeContent[0]
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]    
    ranRes=GetRanWord(thisGroupId,thisWord)
    if ranRes is  None :
        return
    else:
        ranRes=ranRes#.replace('$91;','[').replace('$93;',']').replace('=','$eql;').replace(':','$mh;')
    if not ranRes is None:
        await readRanWord.finish(Message(ranRes))
    else:
        return

# msgTest=on_message(priority=50,block=False)
# @msgTest.handle()
# async def msgTest_handle(bot: Bot, event: Event):
#    thisMsgStr=str(event.get_message())#.extract_plain_text()
#    await msgTest.send(thisMsgStr)



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
