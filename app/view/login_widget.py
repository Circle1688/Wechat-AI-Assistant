import json
import time
import winreg

from PySide6.QtCore import Qt, QUrl, QSize, QThread, Signal, QTimer
from PySide6.QtGui import QPixmap, QIcon, QColor
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget, QApplication
from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase, PasswordLineEdit, BodyLabel, CheckBox, PrimaryPushButton,
                            IndeterminateProgressBar)
from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor
from qfluentwidgets import FluentTranslator, SplitTitleBar

from app.view import shared
from app.view.main_window import MainWindow
import robot
from wcferry import Wcf
from app.view.requestTh import RequestTh

current_version = '1.0.0131'

def get_wx_version():
    """获取微信版本号"""

    try:
        # 打开注册表上下文
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Tencent\WeChat", 0, winreg.KEY_READ) as key:
            # 读取版本号：10进制
            int_version = winreg.QueryValueEx(key, "Version")[0]

            # 转16进制字符串
            hex_version = hex(int_version)

            # 去掉0x
            hex_str = hex_version[2:]

            # 把第一个字符（最高位）替换为 0
            new_hex_str = "0" + hex_str[1:]

            # 转回10进制
            new_hex_num = int(new_hex_str, 16)

            # 按位还原版本号
            major = (new_hex_num >> 24) & 0xFF
            minor = (new_hex_num >> 16) & 0xFF
            patch = (new_hex_num >> 8) & 0xFF
            build = (new_hex_num >> 0) & 0xFF

            # 拼接版本号
            wx_version = "{}.{}.{}.{}".format(major, minor, patch, build)
            return wx_version
    except Exception as e:
        print("打开注册表失败：{}".format(e))
        return None

class LoginWindow(AcrylicWindow):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        setThemeColor('#1AAD19')
        self.resize(300, 400)

        self.setTitleBar(SplitTitleBar(self))

        self.titleBar.raise_()

        self.setWindowTitle('微信个人助手 - 登录')
        self.setWindowIcon(QIcon("app/resource/images/logo.png"))
        self.windowEffect.setMicaEffect(self.winId())

        # self.topLayout = QHBoxLayout(self)
        # self.topLayout.setSpacing(0)
        # self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout = QVBoxLayout(self)
        self.rightLayout.setContentsMargins(100, 50, 100, 10)

        # self.topLayout.addWidget(side)
        #
        # self.topLayout.addLayout(self.rightLayout)
        self.rightLayout.addSpacing(30)
        self.logo_layout = QHBoxLayout(self)
        logo = QLabel(pixmap=QPixmap("app/resource/images/logo.png"),
                      scaledContents=True,
                      maximumSize=QSize(100, 100),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        # add widget to view layout
        self.logo_layout.addWidget(logo)
        self.rightLayout.addLayout(self.logo_layout)

        self.login_btn = PrimaryPushButton(text=self.tr('登录'))

        self.rightLayout.addSpacing(100)

        self.rightLayout.addWidget(self.login_btn)

        self.bar = IndeterminateProgressBar(self)


        # Spacing()
        # self.rightLayout.addSpacing(self.login_btn.height() - self.bar.height())
        self.rightLayout.addWidget(self.bar)
        self.bar.setVisible(False)

        self.rightLayout.addSpacing(20)

        v_label = BodyLabel(self.tr('v' + current_version))
        v_label.setAlignment(Qt.AlignCenter)
        v_label.setTextColor(QColor(100, 100, 100))

        self.rightLayout.addStretch()

        self.rightLayout.addWidget(v_label)

        self.login_btn.clicked.connect(self.start)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        wx_version = get_wx_version()
        if not wx_version:
            w = MessageBox('警告', '当前电脑未安装微信客户端，请前往官网下载 3.9.2.23 版本微信客户端', self.window())
            w.exec()
            self.close()
        else:
            if wx_version != '3.9.2.23':
                w = MessageBox('警告', '当前安装的微信版本不受支持，请前往官网下载 3.9.2.23 版本微信客户端', self.window())
                w.exec()
                self.close()




    def start(self):
        self.login_btn.setVisible(False)
        self.bar.setVisible(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.login)
        self.timer.setSingleShot(True)
        self.timer.setInterval(100)
        self.timer.start()

    def finish_get_user_info(self, is_success, user_info):
        if is_success:
            json_data = json.loads(user_info)
            if current_version in json_data['versions']:
                shared.userInfo = json_data  # 更新用户信息
                self.close()
                w = MainWindow(self.wcf)
            else:
                w = MessageBox('警告', '需要更新必要的新版本，即将退出', self.window())
                w.exec()
                self.close()
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def login(self):
        self.wcf = Wcf(debug=True)
        if self.wcf.is_login():
            user_info = self.wcf.get_user_info()
            wxid = user_info['wxid']
            mobile = user_info['mobile']
            name = user_info['name']
            url = shared.get_info_url
            json_data = {'wxid': wxid, 'name': name, 'mobile': mobile}
            self.userth = RequestTh(url, json_data, 'post')
            self.userth.finish.connect(self.finish_get_user_info)
            self.userth.start()

