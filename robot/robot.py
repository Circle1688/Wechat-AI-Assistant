import re
import time
import xml.etree.ElementTree as ET
from wcferry import Wcf, WxMsg
import logging
from queue import Empty
from threading import Thread

__version__ = "39.0.10.1"
logging.basicConfig(level=logging.DEBUG)

class Robot:
    def __init__(self, wcf: Wcf) -> None:
        self.wcf = wcf
        self.LOG = logging.getLogger("Robot")
        self.wxid = self.wcf.get_self_wxid()
        self.allContacts = self.getAllContacts()

    def toChitchat(self, msg: WxMsg) -> bool:
        """闲聊
        """
        # rsp = '你好呀'
        message = msg.content
        if "小红书" in message:
            rsp = "您好，您是想咨询小朋友的钢琴课程吗"
            time.sleep(1)
            self.sendTextMsg(rsp, msg.sender)
        elif "收费" in message:
            rsp = "我给您一些课程资料，请稍等"
            time.sleep(1)
            self.sendTextMsg(rsp, msg.sender)
            time.sleep(2)
            self.wcf.send_image(r"E:\AI\Wechat-AI-Assistant\piano.jpg", msg.sender)
            rsp = "如果方便的话，我和您通个电话，为您介绍下具体内容？"
            time.sleep(1)
            self.sendTextMsg(rsp, msg.sender)
        elif "电话" in message:
            rsp = "好的，请稍等片刻"
            time.sleep(1)
            self.sendTextMsg(rsp, msg.sender)

        # self.sendTextMsg(rsp, msg.sender)
        return True

    def processMsg(self, msg: WxMsg) -> None:
        """当接收到消息的时候，会调用本方法。如果不实现本方法，则打印原始消息。
        此处可进行自定义发送的内容,如通过 msg.content 关键字自动获取当前天气信息，并发送到对应的群组@发送者
        群号：msg.roomid  微信ID：msg.sender  消息内容：msg.content
        content = "xx天气信息为："
        receivers = msg.roomid
        self.sendTextMsg(content, receivers, msg.sender)
        """
        # 非群聊信息，按消息类型进行处理
        if msg.type == 37:  # 好友请求
            self.autoAcceptFriendRequest(msg)

        elif msg.type == 10000:  # 系统信息
            self.sayHiToNewFriend(msg)

        elif msg.type == 0x01:  # 文本消息
            # 让配置加载更灵活，自己可以更新配置。也可以利用定时任务更新。
            # if msg.from_self():
            #     if msg.content == "^更新$":
            #         self.config.reload()
            #         self.LOG.info("已更新")
            # else:
            self.toChitchat(msg)  # 闲聊

    def enableReceivingMsg(self) -> None:
        def innerProcessMsg(wcf: Wcf):
            while wcf.is_receiving_msg():
                try:
                    msg = wcf.get_msg()
                    self.LOG.info(msg)
                    self.processMsg(msg)
                except Empty:
                    continue  # 空消息
                except Exception as e:
                    self.LOG.error(f"Receiving message error: {e}")
        self.wcf.enable_receiving_msg()
        Thread(target=innerProcessMsg, name='GetMessage', args=(self.wcf,), daemon=True).start()

    def sendTextMsg(self, msg: str, receiver: str, at_list: str = "") -> None:
        """ 发送消息
        :param msg: 消息字符串
        :param receiver: 接收人wxid或者群id
        :param at_list: 要@的wxid, @所有人的wxid为：notify@all
        """
        # msg 中需要有 @ 名单中一样数量的 @
        ats = ""
        if at_list:
            if at_list == "notify@all":  # @所有人
                ats = " @所有人"
            else:
                wxids = at_list.split(",")
                for wxid in wxids:
                    # 根据 wxid 查找群昵称
                    ats += f" @{self.wcf.get_alias_in_chatroom(wxid, receiver)}"

        # {msg}{ats} 表示要发送的消息内容后面紧跟@，例如 北京天气情况为：xxx @张三
        if ats == "":
            self.LOG.info(f"To {receiver}: {msg}")
            self.wcf.send_text(f"{msg}", receiver, at_list)
        else:
            self.LOG.info(f"To {receiver}: {ats}\r{msg}")
            self.wcf.send_text(f"{ats}\n\n{msg}", receiver, at_list)

    def getAllContacts(self) -> dict:
        """
        获取联系人（包括好友、公众号、服务号、群成员……）
        格式: {"wxid": "NickName"}
        """
        contacts = self.wcf.query_sql("MicroMsg.db", "SELECT UserName, NickName FROM Contact;")
        return {contact["UserName"]: contact["NickName"] for contact in contacts}

    def keepRunningAndBlockProcess(self) -> None:
        """
        保持机器人运行，不让进程退出
        """
        while True:
            # self.runPendingJobs()
            time.sleep(1)

    def autoAcceptFriendRequest(self, msg: WxMsg) -> None:
        try:
            xml = ET.fromstring(msg.content)
            v3 = xml.attrib["encryptusername"]
            v4 = xml.attrib["ticket"]
            scene = int(xml.attrib["scene"])
            self.wcf.accept_new_friend(v3, v4, scene)

        except Exception as e:
            self.LOG.error(f"同意好友出错：{e}")

    def sayHiToNewFriend(self, msg: WxMsg) -> None:
        nickName = re.findall(r"你已添加了(.*)，现在可以开始聊天了。", msg.content)
        if nickName:
            # 添加了好友，更新好友列表
            self.allContacts[msg.sender] = nickName[0]
            self.sendTextMsg("您好", msg.sender)

    def getAllFriends(self):
        return self.wcf.get_friends()
