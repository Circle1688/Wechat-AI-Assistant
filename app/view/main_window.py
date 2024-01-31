# coding: utf-8
import datetime
import json
import time
from typing import List

import qrcode
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices, QPixmap, QColor
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget, QLabel, QSizePolicy

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen, InfoBar, InfoBarIcon, InfoBarPosition, MessageBoxBase, BodyLabel,
                            SubtitleLabel, CaptionLabel)
from qfluentwidgets import FluentIcon as FIF

from . import shared
from .gallery_interface import GalleryInterface
from .home_interface import HomeInterface
from .control_interface import ControlInterface
from .character_interface import CharacterInterface
from .massive_interface import MassiveInterface
from .requestTh import RequestTh

# from .basic_input_interface import BasicInputInterface
# from .date_time_interface import DateTimeInterface
# from .dialog_interface import DialogInterface
# from .layout_interface import LayoutInterface
# from .icon_interface import IconInterface
# from .material_interface import MaterialInterface
# from .menu_interface import MenuInterface
# from .navigation_view_interface import NavigationViewInterface
# from .scroll_interface import ScrollInterface
# from .status_info_interface import StatusInfoInterface
from .setting_interface import SettingInterface
# from .text_interface import TextInterface
# from .view_interface import ViewInterface
from .contact_interface import ContactInterface
from ..common.config import ZH_SUPPORT_URL, EN_SUPPORT_URL, cfg
from ..common.icon import Icon
from ..common.signal_bus import signalBus
from ..common.translator import Translator
from ..common import resource
from ..view.user_info_dialog import UserInfoMessageBox
from wcferry import Wcf
from PIL import ImageQt

class PayFailedMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('提示'), self)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(BodyLabel(self.tr('支付未成功'), self))

        # change the text of button
        self.yesButton.setText(self.tr('再试一次'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(360)

class PayInfoMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, img, amount, category, valid, parent=None):
        super().__init__(parent)


        self.logo_layout = QHBoxLayout(self)

        pixmap = QPixmap.fromImage(ImageQt.ImageQt(img))

        qrcode = QLabel(pixmap=pixmap,
                      scaledContents=True,
                      maximumSize=QSize(200, 200),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))
        t_l = BodyLabel(self.tr('打开微信扫一扫'))
        t_l.setAlignment(Qt.AlignCenter)
        self.viewLayout.setSpacing(0)
        self.viewLayout.addSpacing(30)
        self.viewLayout.addWidget(t_l)
        self.viewLayout.setAlignment(Qt.AlignCenter)
        # add widget to view layout
        # self.viewLayout.addSpacing(5)

        self.logo_layout.addWidget(qrcode)

        self.viewLayout.addLayout(self.logo_layout)

        b_l = BodyLabel(self.tr('付款金额 %.2f 元升级成 %s 会员' % (amount / 100, category)))
        b_l.setAlignment(Qt.AlignCenter)

        v_l = CaptionLabel(self.tr(f'现在付款，有效期至{get_end_time_str(time.time(), valid)}， 共 {valid} 天'))
        v_l.setAlignment(Qt.AlignCenter)
        v_l.setTextColor(QColor(100, 100, 100))

        # self.viewLayout.addSpacing(5)

        self.viewLayout.addWidget(b_l)
        self.viewLayout.addSpacing(5)
        self.viewLayout.addWidget(v_l)

        self.viewLayout.addSpacing(30)


        # change the text of button
        self.yesButton.setText(self.tr('我已付款'))

        self.widget.setMinimumWidth(360)

def get_end_time_str(current_timestamp, valid_days):
    valid = datetime.datetime.utcfromtimestamp(current_timestamp) + datetime.timedelta(days=valid_days)
    valid = valid.strftime('%Y年%m月%d日%H时%M分')
    return valid

class MainWindow(FluentWindow):

    def __init__(self, wcf: Wcf):
        super().__init__()
        self.initWindow()

        self.wcf = wcf
        self.wxid = self.wcf.get_self_wxid()

        # create sub interface
        # self.homeInterface = HomeInterface(self)
        # self.controlInterface = ControlInterface(self)
        # self.characterInterface = CharacterInterface(self)
        # self.contactInterface = ContactInterface(self)
        self.massiveInterface = MassiveInterface(wcf, self)

        # self.iconInterface = IconInterface(self)
        # self.basicInputInterface = BasicInputInterface(self)
        # self.dateTimeInterface = DateTimeInterface(self)
        # self.dialogInterface = DialogInterface(self)
        # self.layoutInterface = LayoutInterface(self)
        # self.menuInterface = MenuInterface(self)
        # self.materialInterface = MaterialInterface(self)
        # self.navigationViewInterface = NavigationViewInterface(self)
        # self.scrollInterface = ScrollInterface(self)
        # self.statusInfoInterface = StatusInfoInterface(self)
        self.settingInterface = SettingInterface(self)
        # self.textInterface = TextInterface(self)
        # self.viewInterface = ViewInterface(self)

        # enable acrylic effect
        self.navigationInterface.setAcrylicEnabled(True)

        self.connectSignalToSlot()

        # add items to navigation interface
        self.initNavigation()
        self.splashScreen.finish()

        w = UserInfoMessageBox(parent=self.window())
        w.exec()

    def connectSignalToSlot(self):
        signalBus.micaEnableChanged.connect(self.setMicaEffectEnabled)
        signalBus.switchToSampleCard.connect(self.switchToSample)
        signalBus.supportSignal.connect(self.onSupport)

    def initNavigation(self):
        # add navigation items
        t = Translator()
        # self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        # self.addSubInterface(self.iconInterface, Icon.EMOJI_TAB_SYMBOLS, t.icons)
        # self.navigationInterface.addSeparator()
        #
        pos = NavigationItemPosition.SCROLL
        # self.addSubInterface(self.basicInputInterface, FIF.CHECKBOX,t.basicInput, pos)
        # self.addSubInterface(self.dateTimeInterface, FIF.DATE_TIME, t.dateTime, pos)
        # self.addSubInterface(self.dialogInterface, FIF.MESSAGE, t.dialogs, pos)
        # self.addSubInterface(self.layoutInterface, FIF.LAYOUT, t.layout, pos)
        # self.addSubInterface(self.materialInterface, FIF.PALETTE, t.material, pos)
        # self.addSubInterface(self.menuInterface, Icon.MENU, t.menus, pos)
        # self.addSubInterface(self.navigationViewInterface, FIF.MENU, t.navigation, pos)
        # self.addSubInterface(self.scrollInterface, FIF.SCROLL, t.scroll, pos)
        # self.addSubInterface(self.statusInfoInterface, FIF.CHAT, t.statusInfo, pos)
        # self.addSubInterface(self.textInterface, Icon.TEXT, t.text, pos)
        # self.addSubInterface(self.viewInterface, Icon.GRID, t.view, pos)
        # self.addSubInterface(self.controlInterface, FIF.CHECKBOX, self.tr('控制面板'), pos)
        # self.addSubInterface(self.characterInterface, FIF.ROBOT, self.tr('人设'), pos)
        # self.addSubInterface(self.contactInterface, FIF.PEOPLE, self.tr('联系人'), pos)
        self.addSubInterface(self.massiveInterface, FIF.CHAT, self.tr('群发助手'), pos)

        # add custom widget to bottom
        self.navigationInterface.addWidget(
            routeKey='avatar',
            widget=NavigationAvatarWidget('User', 'app/resource/images/avatar.png'),
            onClick=self.showUserInfoDialog,
            position=NavigationItemPosition.BOTTOM,
        )
        # add custom widget to bottom
        # self.navigationInterface.addItem(
        #     routeKey='price',
        #     icon=Icon.PRICE,
        #     text=t.price,
        #     onClick=self.onSupport,
        #     selectable=False,
        #     tooltip=t.price,
        #     position=NavigationItemPosition.BOTTOM
        # )
        self.addSubInterface(
            self.settingInterface, FIF.SETTING, self.tr('Settings'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(960, 1010)
        self.setMinimumWidth(760)
        self.setWindowIcon(QIcon("app/resource/images/logo.png"))
        self.setWindowTitle('微信个人助手')

        self.setMicaEffectEnabled(cfg.get(cfg.micaEnabled))

        # create splash screen
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(106, 106))
        self.splashScreen.raise_()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        self.show()
        QApplication.processEvents()

    def onSupport(self):
        language = cfg.get(cfg.language).value
        if language.name() == "zh_CN":
            QDesktopServices.openUrl(QUrl(ZH_SUPPORT_URL))
        else:
            QDesktopServices.openUrl(QUrl(EN_SUPPORT_URL))

    def resizeEvent(self, e):
        super().resizeEvent(e)
        if hasattr(self, 'splashScreen'):
            self.splashScreen.resize(self.size())

    def switchToSample(self, routeKey, index):
        """ switch to sample """
        interfaces = self.findChildren(GalleryInterface)
        for w in interfaces:
            if w.objectName() == routeKey:
                self.stackedWidget.setCurrentWidget(w, False)
                w.scrollToCard(index)

    def finish_get_user_info(self, is_success, user_info):
        """ finish get user info """
        if is_success:
            json_data = json.loads(user_info)
            shared.userInfo = json_data  # 更新用户信息
            w = UserInfoMessageBox(parent=self.window())
            w.exec()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def showUserInfoDialog(self):
        json_data = {'wxid': self.wxid}
        self.userth = RequestTh(shared.get_info_url, json_data, 'post')
        self.userth.finish.connect(self.finish_get_user_info)
        self.userth.start()

    def finish_save(self, is_success, text):
        if not is_success:
            w = MessageBox('警告', '网络连接发生错误，用户配置将失去同步', self.window())
            w.exec()
        print('清理环境')
        self.wcf.cleanup()

    def closeEvent(self, e):
        # self.massiveInterface.save_contact_config()  # 保存设置
        json_data = {'wxid': self.wxid, 'contactconfig': json.dumps(shared.contactConfigs)}
        self.saveth = RequestTh(shared.save_info_url, json_data, 'post')
        self.saveth.finish.connect(self.finish_save)
        self.saveth.start()

    def query_close_pay_user_info(self, is_success, text):
        if is_success:
            if json.loads(text)['category'] != 'NORMAL':
                w = MessageBox('提示', f"该订单已支付，恭喜您成为 {json.loads(text)['category']} 会员，有效期至{get_end_time_str(json.loads(text)['createtime'], json.loads(text)['valid'])}， 共 {json.loads(text)['valid']} 天",
                               self.window())
                w.exec()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def close_pay(self, is_success, text):
        if is_success:
            message = json.loads(text)['message']
            if message == '':
                w = PayFailedMessageBox(self.window())
                if w.exec():
                    self.upgrade_user()
                else:
                    self.show_warn_info_bar('取消支付')

            elif message == '该订单已支付':
                json_data = {'wxid': self.wxid}
                self.closequeryth = RequestTh(shared.get_info_url, json_data, 'post')
                self.closequeryth.finish.connect(self.query_close_pay_user_info)
                self.closequeryth.start()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def get_pay_qrcode(self, is_success, text):
        if is_success:
            url = json.loads(json.loads(text)['message'])['code_url']
            out_trade_no = json.loads(text)['out_trade_no']
            amount = json.loads(text)['amount']
            category = json.loads(text)['category']
            valid = json.loads(text)['valid']
            img = qrcode.make(url)
            w = PayInfoMessageBox(img, amount, category, valid, self.window())
            w.exec()
            self.closeth = RequestTh(shared.close_url, {'wxid': self.wxid, 'out_trade_no': out_trade_no, 'category': category}, 'post')
            self.closeth.finish.connect(self.close_pay)
            self.closeth.start()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def upgrade_user(self):
        json_data = {'wxid': self.wxid}
        self.userth = RequestTh(shared.get_info_url, json_data, 'post')
        self.userth.finish.connect(self.finish_query_upgrade_user)
        self.userth.start()

    def finish_query_upgrade_user(self, is_success, text):
        if is_success:
            if json.loads(text)['category'] == 'NORMAL':
                self.request_pay()
            elif json.loads(text)['category'] == 1:
                w = MessageBox('提示', f"恭喜您成为 {json.loads(text)['category']} 会员，有效期{json.loads(text)['valid']}天", self.window())
                w.exec()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def request_pay(self):
        json_data = {'wxid': self.wxid, 'category': 'VIP0'}
        self.payth = RequestTh(shared.pay_url, json_data, 'post')
        self.payth.finish.connect(self.get_pay_qrcode)
        self.payth.start()

    def show_warn_info_bar(self, content):
        infoBar = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=self.tr('警告'),
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            duration=2000,
            position=InfoBarPosition.TOP_RIGHT,
            parent=self.window()
        )
        infoBar.show()

