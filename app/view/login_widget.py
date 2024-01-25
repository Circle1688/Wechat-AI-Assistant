from PySide6.QtCore import Qt, QUrl, QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout
from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase, PasswordLineEdit, BodyLabel, CheckBox, HyperlinkButton)

class LoginMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.nameLineEdit = LineEdit(self)
        self.passwordLineEdit = PasswordLineEdit(self)

        label_username = BodyLabel(self.tr('用户名'))
        label_pwd = BodyLabel(self.tr('密码'))
        self.remember_pwd = CheckBox(self.tr('记住密码'))
        self.register_btn = HyperlinkButton(text=self.tr('注册用户'), url='')
        self.find_pwd_btn = HyperlinkButton(text=self.tr('找回密码'), url='')

        self.logo_layout = QHBoxLayout(self)
        self.h_layout = QHBoxLayout(self)
        self.h_layout2 = QHBoxLayout(self)

        logo = QLabel(pixmap=QPixmap("app/resource/images/logo.png"),
                      scaledContents=True,
                      maximumSize=QSize(100, 100),
                      sizePolicy=QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding))

        # add widget to view layout
        self.logo_layout.addWidget(logo)
        self.viewLayout.addLayout(self.logo_layout)

        self.h_layout.addWidget(label_username)
        self.h_layout.addWidget(self.register_btn)
        self.viewLayout.addLayout(self.h_layout)

        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addWidget(label_pwd)
        self.viewLayout.addWidget(self.passwordLineEdit)
        self.h_layout2.addWidget(self.remember_pwd)
        self.h_layout2.addWidget(self.find_pwd_btn)
        self.viewLayout.addLayout(self.h_layout2)


        # change the text of button
        self.yesButton.setText(self.tr('登录'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)
        self.passwordLineEdit.textChanged.connect(self._validateUrl)

    def _validateUrl(self, text):
        self.yesButton.setEnabled(QUrl(text).isValid())
