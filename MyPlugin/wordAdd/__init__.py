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
ini_absolute_path = "./MyPluginData/WolfWordAdd/WordDB.txt"#'C:\\Users\\Scedovah\\Desktop\\WDB\\WordDB.txt'
dim_absolute_path = "./MyPluginData/WolfWordAdd/WordDim.txt"#'C:\\Users\\Scedovah\\Desktop\\WDB\\WordDim.txt'

def ReturnStrList(thisStr):
    results = []
    # x + 1 表示子串的长度
    for x in range(len(thisStr)):
        # i 表示滑窗长度
        for i in range(len(thisStr) - x):
            results.append(thisStr[i:i + x + 1])
    return results


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
        print('新群号已创建')
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
        conf.set(groupId,targetWord,f'&Nex&{newContent}')
        thisContent= conf.get(groupId, targetWord)
        o=open(ini_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
        return f'新词条添加成功！'

def CutWord(groupId,targetWord,newContent)->str:
    targetWord=str(targetWord).replace('[cq','[CQ')
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(open(ini_absolute_path,encoding='utf-8'))  #指定encoding='utf-8'
    conf.add_section(groupId)#添加section
    if not conf.has_section(groupId) :
        conf.add_section(groupId)#添加section
        o=open(ini_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
        print('新群号已创建')
    conf.clear
    conf.read(ini_absolute_path,encoding='utf-8')  
    if  conf.has_option(groupId, targetWord) :
        wordList=GetWord(groupId,targetWord)
        if newContent in wordList :
            conf.read(ini_absolute_path,encoding='utf-8')
            thisContent= conf.get(groupId, targetWord)
            thisContent=thisContent.replace(f'&Nex&{newContent}','')
            conf.set(groupId,targetWord,f'{thisContent}')
            o=open(ini_absolute_path, "w",encoding='utf-8') 
            conf.write(o)
            o.close()
            return f'删减成功！'
        else:
            return '未找到该记录！'

def GetWord(groupId,targetWord)->str:
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 指定encoding='utf-8'
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                thisContent= conf.get(groupId, targetWord)
                contentList=thisContent.replace('&Nex&','\n')
                return contentList
            else:
                return f'词条不存在！'
    else:
        return f'词条不存在！'

def GetIsDim(groupId,targetWord)->str:
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(dim_absolute_path,encoding='utf-8')  # 指定encoding='utf-8'
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                thisContent= conf.get(groupId, targetWord)
                contentList=thisContent.replace('&Nex&','\n')
                return str(contentList[0])
            else:
                return f'词条不存在！'
    else:
        return f'词条不存在！'

def GetRanWord(groupId,targetWord) ->str:
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    targetWord=targetWord
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                    thisContent= conf.get(groupId, targetWord)
                    contentList=thisContent.split('&Nex&')
                    resReturn=contentList[random.randint(0,len(contentList)-1)]
                    if resReturn=='':
                        return GetRanWord(groupId,targetWord)
                    if not resReturn=='':
                        return resReturn
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

def GetAllWord(groupId):
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(ini_absolute_path,encoding='utf-8')  # 指定encoding='utf-8'
    keys = conf.options(groupId)
    return keys

def DimWord(groupId,thisStr):
    keys = GetAllWord(groupId)
    for myKey in keys:
        if myKey in thisStr:
            return GetRanWord(groupId,myKey)

def SetDim(groupId,targetWord,newContent):
    targetWord=str(targetWord).replace('[cq','[CQ')
    conf = ConfigParser()  # 实例化一个ConfigParser对象
    conf.read(open(dim_absolute_path,encoding='utf-8'))  #指定encoding='utf-8'
    conf.add_section(groupId)#添加section
    if not conf.has_section(groupId) :
        conf.add_section(groupId)#添加section
        o=open(dim_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
    conf.clear
    conf.read(dim_absolute_path,encoding='utf-8')  
    if  conf.has_option(groupId, targetWord) :
        wordList=GetIsDim(groupId,targetWord)
        if not newContent == wordList :
            conf.read(dim_absolute_path,encoding='utf-8')
            thisContent= conf.get(groupId, targetWord)
            conf.set(groupId,targetWord,f'{newContent}')
            o=open(dim_absolute_path, "w",encoding='utf-8') 
            conf.write(o)
            o.close()
            print(f'Dim = {thisContent}')
            return f'设置匹配模式成功！'
        if newContent == wordList :
            return '匹配模式未改变！'
    conf.clear
    conf.read(dim_absolute_path,encoding='utf-8')  
    if  not  conf.has_option(groupId, targetWord) :
        conf.set(groupId,targetWord,newContent)
        thisContent= conf.get(groupId, targetWord)
        o=open(dim_absolute_path, "w",encoding='utf-8') 
        conf.write(o)
        o.close()
        return f'设置匹配模式成功！'




saveWord = on_startswith(['添加词条%'],priority=50)# 创建消息关键词匹配事件响应器
@saveWord.handle()
async def saveWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    thisGroupId = event.get_session_id().split("_")[1] 
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=thisWholeContent[0]
    if thisWord == '':
        await saveWord.finish(Message(f'添加词条名称为空，请检查！'))
    thisContent=thisWholeContent[1]
    if thisContent == '':
        await saveWord.finish(Message(f'添加词条内容为空，请检查！'))
    passport1=1
    passport2=1
    for ch in thisWord:
        if not ch ==' ':
            passport1=1
            break
    for ch in thisContent:
        if not ch ==' ':
            passport2=1
            break
    # if thisWord[0]==' ':
    #     await saveWord.finish(Message(f'词条名称不允许以空格开头！'))
    # if passport1 == 0 or passport2 == 0:
    #     await saveWord.finish(Message(f'词条名称或词条内容不允许全为空格！'))
    if passport1 == 1 and passport2 == 1:
        isDim='0' 
        if len(thisWholeContent) > 2 :
            isDim=thisWholeContent[2]
            if isDim=='模糊':
                isDim='1'
            if isDim=='全文':
                isDim='0'   
            if not isDim == '模糊':
                if not isDim == '全文':
                    isDim='0' 
        thisWord=(thisWord).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace(':','$mh;').replace(' ','$blank;')#.replace('cq:','cq = ')
        #thisContent=repr(thisContent)
        #thisGroupId = event.get_session_id().split("_")[1]       
        #await saveWord.send(Message(f'添加的文本是 {thisWord}')) 
        #await saveWord.send(Message(f'添加的内容是 {thisContent}')) 
        #await saveWord.send(Message(
        SetDim(thisGroupId,thisWord,isDim)#))
        await saveWord.finish(Message(f'{cqAt(event.get_user_id())}{AddWord(thisGroupId,thisWord,thisContent)}'))


setWord = on_startswith(['设置词条%'],priority=50)# 创建消息关键词匹配事件响应器
@setWord.handle()
async def setWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=thisWholeContent[0]
    isDim=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1] 
    if isDim=='模糊':
        isDim='1'
    if isDim=='全文':
        isDim='0'   
    await setWord.finish(Message(f'{cqAt(event.get_user_id())}{SetDim(thisGroupId,thisWord,isDim)}'))

readWord = on_startswith(['查看词条%'],priority=50,block=True)# 创建消息关键词匹配事件响应器
@readWord.handle()
async def readWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=(thisWholeContent[0]).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('[CQ','[cq').replace(':','$mh;').replace(' ','$blank;')#.replace('cq:','cq = ')
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    #await readWord.send(f'正在查询词条{thisWord}...')
    await readWord.finish(Message(f'词条查询结果为:{GetWord(thisGroupId,thisWord)}'))

#================================================================================
readAllWord = on_startswith(['查看本群词条'],priority=50)# 创建消息关键词匹配事件响应器
@readAllWord.handle()
async def readAllWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisGroupId = event.get_session_id().split("_")[1]     
    wordList=GetAllWord(thisGroupId)#.replace('$91;','[').replace('$93;',']').replace('$eql;','=').replace('$mh;',':')
    wordStr=f'本群({thisGroupId})词条列表：'
    for word in wordList:
        wordStr=wordStr+'\n'+word
    wordStr=wordStr.replace('$91;','[').replace('$93;',']').replace('$eql;','=').replace('$mh;',':').replace('cq','CQ').replace('$blank;',' ')
    await readAllWord.finish(Message(wordStr))
#================================================================================

delWord = on_startswith(['删除词条%'],priority=50)# 创建消息关键词匹配事件响应器
@delWord.handle()
async def delWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=(thisWholeContent[0]).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('CQ','cq').replace(':','$mh;').replace(' ','$blank;')#.replace('cq:','cq = ')
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    await delWord.finish(Message(DelWord(thisGroupId,thisWord)))

cutWord = on_startswith(['删减词条%'],priority=50)# 创建消息关键词匹配事件响应器
@cutWord.handle()
async def cutWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    thisGroupId = event.get_session_id().split("_")[1] 
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('%')
    thisWord=(thisWholeContent[0]).replace('[','$91;').replace(']','$93;').replace('=','$eql;').replace('CQ','cq').replace(':','$mh;').replace(' ','$blank;')#.replace('cq:','cq = ')
    if thisWord == '':
        await cutWord.finish(Message(f'删减词条名称为空，请检查！'))
    thisContent=thisWholeContent[1]
    if thisContent == '':
        await cutWord.finish(Message(f'删减词条内容为空，请检查！'))
    await cutWord.finish(Message(f'{CutWord(thisGroupId,thisWord,thisContent)}'))

#root_dir=os.path.dirname(os.path.pardir('.')) 

readRanWord = on_message(priority=51,block=False)# 创建消息关键词匹配事件响应器
@readRanWord.handle()
async def readRanWord_handle(bot: Bot, event: GroupMessageEvent):#异步定义
    thisMsgStr=str(event.get_message())
    thisGroupId = event.get_session_id().split("_")[1]    
    #eventContent=str(event)
    #await saveWord.send(Message(f'event是 {eventContent}'))  
    #thisMsgStr=event.get_message().extract_plain_text()
    #thisWholeContent=str(thisMsgStr).split('#')
    thisWord=(thisMsgStr).replace('[','$91;').replace(']','$93;').replace('CQ','cq').replace('=','$eql;').replace(':','$mh;').replace(' ','$blank;')#.replace('cq:','cq = ')
    wordList=ReturnStrList(thisWord)
    print(wordList)
    for sonWord in wordList:
        #thisWholeContent[0]
        #thisContent=thisWholeContent[1]
        isDim='0'
        isDim=GetIsDim(thisGroupId,sonWord)
        print(f'DIM {isDim}')
        print(f'')
        if isDim=='0':
            ranRes=GetRanWord(thisGroupId,thisWord)
            if ranRes is  None :
                return
            else:
                ranRes=ranRes#.replace('$91;','[').replace('$93;',']').replace('=','$eql;').replace(':','$mh;')
            if not ranRes is None:
                await readRanWord.send(Message(ranRes))
            else:
                return
        if isDim=='1':
            #await readRanWord.send(Message(DimWord(thisGroupId,thisMsgStr)))
            resWord=DimWord(thisGroupId,sonWord)
            if not resWord == None:
                await readRanWord.finish(Message(resWord))

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
