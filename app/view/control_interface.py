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
from ..common.config import cfg

class ControlInterface(GalleryInterface):
    """ control interface """

    def __init__(self, parent=None):
        super().__init__(
            title=self.tr("控制中心"),
            subtitle="管理助手设置等等",
            parent=parent
        )
        self.setObjectName('controlInterface')

        self.assistantGroup = SettingCardGroup(
            self.tr('助手设置'))

        self.switchCard = SwitchSettingCard(
            FIF.POWER_BUTTON,
            self.tr('启用'),
            self.tr('是否启用助手')
        )

        self.wait_timeCard = ComboBoxSettingCard(
            cfg.waitTime,
            FIF.STOP_WATCH,
            self.tr('回复速度'),
            self.tr("控制助手回复的速度"),
            texts=[
                self.tr('慢速'), self.tr('正常'),
                self.tr('快速'), self.tr('秒回')
            ],
            parent=self.assistantGroup
        )

        self.tokenRadiusCard = RangeSettingCard(
            cfg.maxToken,
            FIF.ROBOT,
            self.tr('回复长度'),
            self.tr('控制助手回复的内容长度'),
            self.assistantGroup
        )

        self.assistantGroup.addSettingCard(self.wait_timeCard)
        self.assistantGroup.addSettingCard(self.tokenRadiusCard)

        self.vBoxLayout.addWidget(self.switchCard)
        self.vBoxLayout.addWidget(self.assistantGroup)
