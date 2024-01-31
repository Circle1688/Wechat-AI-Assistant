from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase, PasswordLineEdit, BodyLabel, CheckBox, HyperlinkButton,
                            AvatarWidget, InfoBadge, PrimaryPushButton)

from app.view import shared
import datetime

def get_end_time_str(current_timestamp, valid_days):
    valid = datetime.datetime.utcfromtimestamp(current_timestamp) + datetime.timedelta(days=valid_days)
    valid = valid.strftime('%Y年%m月%d日%H时%M分')
    return valid

def get_remain_days(input_timestamp, end_days):
    input_datetime = datetime.datetime.utcfromtimestamp(input_timestamp)

    current_datetime = datetime.datetime.utcnow()

    time_difference = current_datetime - input_datetime

    return time_difference.days + end_days

class UserInfoMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        createtime = shared.userInfo['createtime']
        self.parent = parent


        label_username = BodyLabel(self.tr(f"绑定微信名:         {shared.userInfo['name']}"))
        label_vip_state = BodyLabel(self.tr('会员状态:  '))




        self.logo_layout = QHBoxLayout(self)

        logo = QLabel(pixmap=QPixmap("app/resource/images/logo.png"),
                      scaledContents=True,
                      maximumSize=QSize(100, 100),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        self.avatar = AvatarWidget(image=QPixmap('app/resource/images/avatar.png'))

        # add widget to view layout
        self.viewLayout.setSpacing(30)
        self.viewLayout.addSpacing(30)


        self.logo_layout.addWidget(self.avatar)
        self.viewLayout.addLayout(self.logo_layout)

        self.viewLayout.addSpacing(30)

        self.viewLayout.addWidget(label_username)

        h_layout = QHBoxLayout()
        h_layout.setAlignment(Qt.AlignLeft)
        h_layout.addWidget(label_vip_state)

        self.upgrade_btn = PrimaryPushButton(self.tr('升级会员'))



        if shared.userInfo['category'] != 'NORMAL':
            label = InfoBadge.success(f"   {shared.userInfo['category']} 会员   ")
            label.setMinimumHeight(25)
            h_layout.addWidget(label)

            label_end_day = BodyLabel(self.tr(
                f"有效期至:            {get_end_time_str(shared.userInfo['createtime'], shared.userInfo['valid'])}"))


            self.remain_day = get_remain_days(createtime, shared.userInfo['valid'])
            if self.remain_day < 0:
                self.remain_day = 0

            label_remain_day = BodyLabel(self.tr(f'剩余天数:            {self.remain_day}天'))
        else:
            label = InfoBadge.info('   普通用户   ')
            label.setMinimumHeight(25)
            h_layout.addWidget(label)

            label_end_day = BodyLabel(self.tr(
                f"有效期至:            -"))

            label_remain_day = BodyLabel(self.tr(f'剩余天数:            -'))

            h_layout.addSpacing(20)

            self.upgrade_btn.clicked.connect(self.upgrade)

            h_layout.addWidget(self.upgrade_btn)
            self.remain_day = shared.userInfo['valid']




        self.viewLayout.addLayout(h_layout)

        self.viewLayout.addWidget(label_end_day)
        self.viewLayout.addWidget(label_remain_day)




        # self.viewLayout.addSpacing(30)

        # self.viewLayout.addWidget(self.logout_btn)


        # change the text of button
        self.yesButton.setText(self.tr('ok'))
        self.cancelButton.setVisible(False)

        self.widget.setMinimumWidth(360)

    def upgrade(self):
        self.parent.upgrade_user()
        self.close()

