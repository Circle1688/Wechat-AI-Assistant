from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase, PasswordLineEdit, BodyLabel, CheckBox, HyperlinkButton,
                            AvatarWidget, InfoBadge)

class UserInfoMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, user_info, parent=None):
        super().__init__(parent)
        self.remain_day = 30
        self.username = user_info['name']

        label_username = BodyLabel(self.tr(f'绑定微信名: {self.username}'))
        label_vip_state = BodyLabel(self.tr('会员状态: '))

        label_remain_day = BodyLabel(self.tr(f'剩余天数: {self.remain_day}天'))

        self.logout_btn = PushButton(self.tr('退出登录'))

        self.logo_layout = QHBoxLayout(self)

        logo = QLabel(pixmap=QPixmap("app/resource/images/logo.png"),
                      scaledContents=True,
                      maximumSize=QSize(100, 100),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.avatar = AvatarWidget(image=QPixmap('app/resource/images/avatar.png'))

        # add widget to view layout
        self.viewLayout.addSpacing(30)

        self.logo_layout.addWidget(self.avatar)
        self.viewLayout.addLayout(self.logo_layout)

        self.viewLayout.addSpacing(30)

        self.viewLayout.addWidget(label_username)

        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(label_vip_state)
        h_layout.addWidget(InfoBadge.success('  V I P  '))
        self.viewLayout.addLayout(h_layout)

        self.viewLayout.addWidget(label_remain_day)

        # self.viewLayout.addSpacing(30)

        # self.viewLayout.addWidget(self.logout_btn)


        # change the text of button
        self.yesButton.setText(self.tr('ok'))
        self.cancelButton.setVisible(False)

        self.widget.setMinimumWidth(360)
