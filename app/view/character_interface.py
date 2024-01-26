from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, HeaderCardWidget, TitleLabel,
                            InfoBar, InfoBarPosition, LineEdit, EditableComboBox, Slider, PushButton)
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
        self.addExampleCard(title='助手名称', widget=self.bot_name_lineedit, stretch=1)

        self.bot_describe_lineedit = LineEdit()
        self.bot_describe_lineedit.setPlaceholderText(self.tr('为你的助手添加一段简短的描述'))
        self.bot_describe_lineedit.setClearButtonEnabled(True)
        self.addExampleCard(title='助手描述', widget=self.bot_describe_lineedit, stretch=1)

        self.bot_character_comboBox = EditableComboBox()
        self.bot_character_comboBox.addItems([self.tr("活泼开朗"),
                                              self.tr("沉着稳重"),
                                              self.tr("善解人意")])
        self.addExampleCard(title='性格预设（可编辑）', widget=self.bot_character_comboBox, stretch=1)

        self.bot_order_lineedit = LineEdit()
        self.bot_order_lineedit.setPlaceholderText(self.tr('你的助手需要处理哪些事情'))
        self.bot_order_lineedit.setClearButtonEnabled(True)
        self.addExampleCard(title='设定', widget=self.bot_order_lineedit, stretch=1)

        self.bot_prologue_lineedit = LineEdit()
        self.bot_prologue_lineedit.setPlaceholderText(self.tr('为你的助手添加一个开场白'))
        self.bot_prologue_lineedit.setClearButtonEnabled(True)
        self.addExampleCard(title='开场白', widget=self.bot_prologue_lineedit, stretch=1)

        self.bot_creative_slider = Slider(Qt.Horizontal)
        self.bot_creative_slider.setRange(0, 100)
        self.bot_creative_slider.setValue(30)
        self.addExampleCard(title='联想能力（越往右越有创造力）', widget=self.bot_creative_slider, stretch=1)

        self.upload_btn = PushButton(self.tr('上传文件'))
        self.addExampleCard(title='知识', widget=self.upload_btn, stretch=0)



