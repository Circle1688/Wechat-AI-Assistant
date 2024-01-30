# coding: utf-8
import json
from typing import List
from PySide6.QtCore import Qt, Signal, QEasingCurve, QUrl, QSize
from PySide6.QtGui import QIcon, QDesktopServices
from PySide6.QtWidgets import QApplication, QHBoxLayout, QFrame, QWidget

from qfluentwidgets import (NavigationAvatarWidget, NavigationItemPosition, MessageBox, FluentWindow,
                            SplashScreen)
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

        self.user_info = self.wcf.get_user_info()

        w = UserInfoMessageBox(self.user_info, parent=self.window())
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
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
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
            w = UserInfoMessageBox(self.user_info, parent=self.window())
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

