from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, HeaderCardWidget, TitleLabel,
                            InfoBar, InfoBarPosition, LineEdit, EditableComboBox, Slider, PushButton, PlainTextEdit,
                            PrimaryPushButton)
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout
from ..common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from .gallery_interface import GalleryInterface

class CharacterInterface(GalleryInterface):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(
            title=self.tr("人设"),
            subtitle="给你的助手赋予生命力吧",
            parent=parent
        )
        self.setObjectName('characterInterface')

        # self.switchCard = SwitchSettingCard(
        #     FIF.POWER_BUTTON,
        #     self.tr('启用'),
        #     self.tr('是否启用助手')
        # )
        #
        # self.vBoxLayout.addWidget(self.switchCard)

        self.bot_name_lineedit = LineEdit()
        self.bot_name_lineedit.setPlaceholderText(self.tr('为你的助手起一个名字'))
        self.bot_name_lineedit.setClearButtonEnabled(True)
        self.addTitleGroup(title='助手名称', subtitle='', widget=self.bot_name_lineedit, stretch=1)

        self.bot_describe_lineedit = PlainTextEdit()
        self.bot_describe_lineedit.setPlaceholderText(self.tr('为你的助手添加一段简短的描述'))
        self.addTitleGroup(title='助手描述', subtitle='', widget=self.bot_describe_lineedit, stretch=1)

        self.bot_character_comboBox = EditableComboBox()
        self.bot_character_comboBox.addItems([self.tr("活泼开朗"),
                                              self.tr("沉着稳重"),
                                              self.tr("善解人意")])
        self.addTitleGroup(title='性格预设', subtitle='可编辑成想要的性格', widget=self.bot_character_comboBox, stretch=1)

        self.bot_order_lineedit = PlainTextEdit()
        self.bot_order_lineedit.setPlaceholderText(self.tr('你的助手需要处理哪些事情'))
        self.addTitleGroup(title='设定', subtitle='例如 你可以做什么 你能帮助我处理什么事情', widget=self.bot_order_lineedit, stretch=1)

        self.bot_prologue_lineedit = PlainTextEdit()
        self.bot_prologue_lineedit.setPlaceholderText(self.tr('为你的助手添加一个开场白'))
        self.addTitleGroup(title='开场白', subtitle='让你的助手充满活力', widget=self.bot_prologue_lineedit, stretch=1)

        self.bot_creative_slider = Slider(Qt.Horizontal)
        self.bot_creative_slider.setRange(0, 100)
        self.bot_creative_slider.setValue(30)
        self.addTitleGroup(title='联想能力', subtitle='越往右越有创造力', widget=self.bot_creative_slider, stretch=1)

        self.upload_btn = PushButton(self.tr('上传文件'))
        self.addTitleGroup(title='知识', subtitle='让你的助手成为业务专家', widget=self.upload_btn, stretch=0)

        self.create_btn = PrimaryPushButton(self.tr('创建助手'))
        self.vBoxLayout.addWidget(self.create_btn)



