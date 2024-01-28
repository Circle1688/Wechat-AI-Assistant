from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget, QApplication
from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase, PasswordLineEdit, BodyLabel, CheckBox, PrimaryPushButton)
from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor
from qfluentwidgets import FluentTranslator, SplitTitleBar
from app.view.main_window import MainWindow
import robot
from wcferry import Wcf

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

        self.login_btn = PrimaryPushButton(text=self.tr('微信扫码登录'))

        self.rightLayout.addSpacing(50)

        self.rightLayout.addWidget(self.login_btn)

        self.login_btn.clicked.connect(self.start)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def start(self):
        self.login()

    def login(self):
        wcf = Wcf(debug=True)
        if wcf.is_login():
            print(wcf.get_self_wxid())
            self.close()
            w = MainWindow(wcf)
