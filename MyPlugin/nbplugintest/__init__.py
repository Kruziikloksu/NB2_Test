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

global_config = get_driver().config
config = Config.parse_obj(global_config)
plugin_config = Config.parse_obj(get_driver().config)

# proDir = os.path.split(os.path.realpath(__file__))[0]
# # proDir = os.path.dirname(os.path.realpath(__file__))  与上面一行代码作用一样
# configPath = os.path.join(proDir, "WordDB.txt")
# path = os.path.abspath(configPath)
ini_absolute_path = 'C:/Users/Scedovah/Desktop/WDB/WordDB.txt'

def AddWord(groupId,targetWord,newContent):
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(open(ini_absolute_path))  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    conf.add_section(groupId)#添加section
    if not conf.has_section(groupId) :
        conf.add_section(groupId)#添加section
        o=open(ini_absolute_path, "w") 
        conf.write(o)
        o.close()
    conf.clear
    conf.read(ini_absolute_path)  
    if  conf.has_option(groupId, targetWord) :
        wordList=GetWord(groupId,targetWord)
        if not newContent in wordList :
            conf.read(ini_absolute_path)
            thisContent= conf.get(groupId, targetWord)
            conf.set(groupId,targetWord,f'{thisContent}&Nex&{newContent}')
            o=open(ini_absolute_path, "w") 
            conf.write(o)
            o.close()
            return '添加成功！'
        else:
            return '该记录已存在，请勿重复添加！'
    conf.clear
    conf.read(ini_absolute_path)  
    if  not  conf.has_option(groupId, targetWord) :
        conf.set(groupId,targetWord,newContent)
        thisContent= conf.get(groupId, targetWord)
        o=open(ini_absolute_path, "w") 
        conf.write(o)
        o.close()
        return '添加成功！'

def GetWord(groupId,targetWord):
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path)  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'

    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                thisContent= conf.get(groupId, targetWord)
                contentList=thisContent.replace('&Nex&','\n')
                return contentList
            else:
                return '该词条不存在！'
    else:
        return '该词条不存在！'

def GetRanWord(groupId,targetWord):
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path)  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                    thisContent= conf.get(groupId, targetWord)
                    contentList=thisContent.split('&Nex&')
                    return contentList[random.randint(0,len(contentList)-1)]

def DelWord(groupId,targetWord):
    conf = ConfigParser()  # 需要实例化一个ConfigParser对象
    conf.read(ini_absolute_path)  # 需要添加上config.ini的路径，不需要open打开，直接给文件路径就读取，也可以指定encoding='utf-8'
    if  conf.has_section(groupId) :
            if  conf.has_option(groupId, targetWord) :
                    conf.remove_option(groupId, targetWord) #删除指定section的key
                    o=open(ini_absolute_path, "w") 
                    conf.write(o)
                    o.close()
                    return '删除成功！'
            return '未找到该词条！'
    return '未找到该词条！'





saveWord = on_startswith(['添加词条#'],priority=50)# 创建消息关键词匹配事件响应器
@saveWord.handle()
async def saveWord_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('#')
    thisWord=thisWholeContent[0]
    thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    #await saveWord.send(Message(thisMsgStr)) 
    await saveWord.finish(Message(AddWord(thisGroupId,thisWord,thisContent)))

readWord = on_startswith(['查看词条#'],priority=50)# 创建消息关键词匹配事件响应器
@readWord.handle()
async def readWord_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('#')
    thisWord=thisWholeContent[0]
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    #await readWord.send(f'正在查询词条{thisWord}...')
    await readWord.finish(Message(GetWord(thisGroupId,thisWord)))

delWord = on_startswith(['删除词条#'],priority=50)# 创建消息关键词匹配事件响应器
@delWord.handle()
async def delWord_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[5:]
    thisWholeContent=str(thisMsgStr).split('#')
    thisWord=thisWholeContent[0]
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]       
    await delWord.finish(Message(DelWord(thisGroupId,thisWord)))

readRanWord = on_keyword([''],priority=51)# 创建消息关键词匹配事件响应器
@readRanWord.handle()
async def readRanWord_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=str(event.get_message())
    #thisMsgStr=event.get_message().extract_plain_text()
    thisWholeContent=str(thisMsgStr).split('#')
    thisWord=thisWholeContent[0]
    #thisContent=thisWholeContent[1]
    thisGroupId = event.get_session_id().split("_")[1]      
    ranRes=GetRanWord(thisGroupId,thisWord)
    if not ranRes is None:
        await readRanWord.finish(Message(ranRes))

















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
    return ''.join([c.replace('o','汪').replace('0', '嗷').replace('1', '呜').replace('2', '呼').replace('3', '噜').replace('4', '嘟').replace('5', '咕').replace('6', '啾').replace('7', '咪').replace(' ', '!') for c in s])
def wolfToMath(s):
    return ''.join([c.replace('汪','o').replace('嗷', '0').replace('呜', '1').replace('呼', '2').replace('噜', '3').replace('嘟', '4').replace('咕', '5').replace('啾', '6').replace('咪', '7').replace('!', ' ') for c in s])
#=================================================================================
wolfHowl = on_startswith(['狼叫'],priority=50)# 创建消息关键词匹配事件响应器
@wolfHowl.handle()
async def wolfHowl_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[2:]
    encodeMsg = longStrTran(thisMsgStr)
    woflMsg = mathToWolf(encodeMsg)
    await wolfHowl.send(Message(woflMsg))


unHowl = on_startswith(['翻译狼叫'],priority=50)# 创建消息关键词匹配事件响应器
@unHowl.handle()
async def unHowl_handle(bot: Bot, event: Event):#异步定义
    thisMsgStr=event.get_message().extract_plain_text()
    thisMsgStr=thisMsgStr[4:]
    mathMsg = wolfToMath(thisMsgStr)
    decodeMsg = longOoTran(mathMsg)
    await unHowl.finish(Message(decodeMsg))




randomFileChoose = on_keyword(['随机图片'],priority=50)# 创建消息关键词匹配事件响应器
@randomFileChoose.handle()
async def randomFileChoose_handle(bot: Bot, event: Event):#异步定义
    randomImagePath=str(RandomFileGet('C:/Users/Scedovah/Desktop/wolves/'))
    await randomFileChoose.finish(Message(cqImg(randomImagePath)))


jrrp = on_keyword(['jrrp','今日人品'],priority=50)# 创建消息关键词匹配事件响应器
@jrrp.handle()
async def jrrp_handle(bot: Bot, event: Event):#异步定义
    rnd = random.Random()
    rnd.seed(int(date.today().strftime("%y%m%d")) + int(event.get_user_id()))
    lucknum = rnd.randint(1,100)
    await jrrp.finish(Message(f'[CQ:at,qq={event.get_user_id()}]今天的人品值是{lucknum}'))

getNum = on_keyword(['获得随机数'],priority=50)# 创建消息关键词匹配事件响应器
@getNum.handle()#使用 handle 装饰器
async def getNum_handle(bot: Bot, event: Event):#异步定义
    randomNum=random.randint(0,100)
    await getNum.finish(Message(f'randomNum is {randomNum}[CQ:face,id=123]'))

getImage = on_keyword(['图片测试'],priority=50)# 创建消息关键词匹配事件响应器
@getImage.handle()#使用 handle 装饰器
async def getImage_handle(bot: Bot, event: Event):#异步定义
    randomNum=random.randint(0,100)
    msg1 = Message('看图')
    msg2 = MessageSegment.image('file:///C:/Users/Scedovah/Desktop/avatar.jpg')
    msg3 = Message(f'{cqAt(event.get_user_id())}')
    msg  = msg3 + msg1 + msg2 + msg3
    await getNum.finish(Message(f'{msg}'))

thisGroupInfo = on_startswith("本群信息",priority=50)
@thisGroupInfo.handle()
async def _(bot: Bot, event: Event):
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

    #await thisGroupInfo.send(thisGroupId)
    await thisGroupInfo.finish(msg)
#/get_group_member_list

thisGroupMemberInfo = on_startswith("我的群信息",priority=50)
@thisGroupMemberInfo.handle()
async def _(bot: Bot, event: Event):
    thisGroupId = event.get_session_id().split("_")[1]
    thisGroupId = event.get_session_id().split("_")[1]

    groupMemberData = await bot.call_api('get_group_member_info',**{
        'group_id' : thisGroupId,
        'user_id'  : event.get_user_id()
    })
    # 对json进行转义
    dataGM = ast.literal_eval(str(groupMemberData))
    msg = f"\
QQ号：{dataGM['user_id']}\n\
昵称：{dataGM['nickname']}\n\
群名片：{dataGM['card']}\n\
入群时间：{dataGM['join_time']}\n\
等级：{dataGM['level']}"   

    #await thisGroupMemberInfo.send(Message(os.path.dirname))
    await thisGroupMemberInfo.finish(msg)

banMan = on_startswith("杀",priority=50)
@banMan.handle()
async def _(bot: Bot, event: Event):
    thisGroupId = event.get_session_id().split("_")[1]
    thisMsgStr=str(event.get_message()).replace(' ','')
    thisMsgStr=thisMsgStr[1:]
    banInfo=str(thisMsgStr[10:]).split(']')[0]
    banInfo2=thisMsgStr.split(']')[1].replace(' ','')
    # await randomFileChoose.send(banInfo)
    # await randomFileChoose.send(banInfo2)
    #杀[CQ:at,qq=1159383775]【禁言0>=<【正则(\d+(\.\d+)?)>=<【内容】】】
    # call_api
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id' : banInfo,
        'duration':  int(banInfo2)*60
    })
saveMan = on_startswith("解禁",priority=50)
@saveMan.handle()
async def _(bot: Bot, event: Event):
    thisGroupId = event.get_session_id().split("_")[1]
    thisMsgStr=str(event.get_message()).replace(' ','')
    thisMsgStr=thisMsgStr[1:]
    banInfo=str(thisMsgStr[10:]).split(']')[0]
    # await randomFileChoose.send(banInfo)
    # await randomFileChoose.send(banInfo2)
    #杀[CQ:at,qq=1159383775]【禁言0>=<【正则(\d+(\.\d+)?)>=<【内容】】】
    # call_api
    await bot.call_api('set_group_ban',**{
        'group_id' : thisGroupId,
        'user_id' : banInfo,
        'duration': 0
    })

 


