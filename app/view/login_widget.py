import json
import time

from PySide6.QtCore import Qt, QUrl, QSize, QThread, Signal, QTimer
from PySide6.QtGui import QPixmap, QIcon
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

class LoginWindow(AcrylicWindow):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(300, 400)

        self.setTitleBar(SplitTitleBar(self))

        self.titleBar.raise_()

        self.setWindowTitle('微信个人助手 - 登录')
        self.setWindowIcon(QIcon(':/gallery/images/logo.png'))
        self.windowEffect.setMicaEffect(self.winId())

        # self.topLayout = QHBoxLayout(self)
        # self.topLayout.setSpacing(0)
        # self.topLayout.setContentsMargins(0, 0, 0, 0)
        self.rightLayout = QVBoxLayout(self)
        self.rightLayout.setContentsMargins(100, 50, 100, 50)

        side = QLabel()
        pixmap = QPixmap("app/resource/images/side.png")
        pixmap.scaled(side.size(), Qt.KeepAspectRatio)
        side.setScaledContents(True)
        side.setPixmap(pixmap)
        side.repaint()

        # self.topLayout.addWidget(side)
        #
        # self.topLayout.addLayout(self.rightLayout)

        self.logo_layout = QHBoxLayout(self)
        logo = QLabel(pixmap=QPixmap("app/resource/images/logo.png"),
                      scaledContents=True,
                      maximumSize=QSize(100, 100),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        # add widget to view layout
        self.logo_layout.addWidget(logo)
        self.rightLayout.addLayout(self.logo_layout)

        self.login_btn = PrimaryPushButton(text=self.tr('登录'))

        self.rightLayout.addSpacing(50)

        self.rightLayout.addWidget(self.login_btn)

        self.login_btn.clicked.connect(self.start)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)


    def start(self):
        self.login_btn.setVisible(False)
        bar = IndeterminateProgressBar(self)
        self.rightLayout.addSpacing(self.login_btn.height() - bar.height())
        self.rightLayout.addWidget(bar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.login)
        self.timer.setSingleShot(True)
        self.timer.setInterval(1000)
        self.timer.start()

    def finish_get_user_info(self, is_success, user_info):
        if is_success:
            json_data = json.loads(user_info)
            shared.userInfo = json_data  # 更新用户信息
            self.close()
            w = MainWindow(self.wcf)
        else:
            w = MessageBox('警告', '网络连接发生错误，即将退出', self.window())
            w.exec()
            self.wcf.cleanup()
            self.close()

    def login(self):
        self.wcf = Wcf(debug=True)
        if self.wcf.is_login():
            wxid = self.wcf.get_self_wxid()
            url = shared.get_info_url
            json_data = {'wxid': wxid}
            self.userth = RequestTh(url, json_data, 'post')
            self.userth.finish.connect(self.finish_get_user_info)
            self.userth.start()

