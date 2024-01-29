import time

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, HeaderCardWidget, TitleLabel,
                            InfoBar, InfoBarPosition, SearchLineEdit, LineEdit, EditableComboBox, Slider, PushButton,
                            PlainTextEdit,
                            TimePicker, CheckBox, PrimaryPushButton, TableWidget, SwitchButton, RadioButton, BodyLabel,
                            CaptionLabel, StateToolTip)
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QFrame, \
    QButtonGroup, QTableWidget, QHeaderView, QAbstractItemView
from ..common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from .gallery_interface import GalleryInterface
from wcferry import Wcf
import json
from ..view import shared



class MassiveInterface(GalleryInterface):
    """ massive interface """

    def __init__(self, wcf: Wcf, parent=None):
        super().__init__(
            title=self.tr("群发助手"),
            subtitle="只有设置了尊称的联系人才能设置群发",
            parent=parent
        )
        self.wcf = wcf
        self.setObjectName('massiveInterface')

        self.vBoxLayout.setSpacing(10)

        shared.contactInfos = self.wcf.get_friends()

        shared.contactConfigs = {}  # 保存的联系人id，尊称，是否群发开关，该配置应该向服务器获取
        self.load_contact_config()  # 本地测试
        self.build_save_dict()  # 同步

        self.show_option_ID = 0  # 显示全部

        self.stateTooltip = None  # 进度提示

        self.send_msg_id = []  # 已发送的msgid


        self.searchLineEdit = SLineEdit(self)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.contactTable = ContactTable(self)
        self.vBoxLayout.addWidget(self.contactTable)
        self.vBoxLayout.addSpacing(20)

        self.content_lineedit = PlainTextEdit()
        self.content_lineedit.setPlaceholderText(self.tr('要发送的消息内容，例如输入：\n值此佳节，给%尊称%拜年，祝新春快乐！\n\n张总收到的就是：\n值此佳节，给张总拜年，祝新春快乐！\n王总收到的就是：\n值此佳节，给王总拜年，祝新春快乐！'))
        self.content_lineedit.setMaximumHeight(150)

        self.add_format_btn = PushButton(self.tr('插入尊称'))
        self.addTitleGroup(title='消息内容', subtitle='要发送的消息内容，支持格式化文本，例如[尊称]，将自动替换为对应联系人的尊称', widget=self.add_format_btn, stretch=0)

        self.vBoxLayout.addWidget(self.content_lineedit)

        self.send_btn = PrimaryPushButton(self.tr('立即发送'))
        self.revo_btn = PushButton(self.tr('全部撤回'))
        self.revo_btn.setEnabled(False)
        h_layout = QHBoxLayout()
        h_layout.setSpacing(10)
        h_layout.setContentsMargins(0, 0, 0, 0)
        h_layout.addStretch()
        h_layout.addWidget(self.revo_btn)
        h_layout.addWidget(self.send_btn)
        self.vBoxLayout.addLayout(h_layout)


        self.searchLineEdit.clearSignal.connect(self.showAll)
        self.searchLineEdit.searchSignal.connect(self.search)

        self.contactTable.show_option.buttonGroup.buttonClicked.connect(self.show_option_changed)

        self.send_btn.clicked.connect(self.send_msg)
        self.add_format_btn.clicked.connect(self.add_format)
        self.revo_btn.clicked.connect(self.revoke_all)

    def revoke_all(self):
        self.stateTooltip = StateToolTip(self.tr('正在撤回刚刚发送的全部消息'), self.tr('请耐心等待'), self.window())
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()
        for msg_id in self.send_msg_id:
            self.wcf.revoke_msg(msg_id)  # 尝试撤回
        # 完成
        self.stateTooltip.setContent(self.tr('已全部撤回') + ' 😆')
        self.stateTooltip.setState(True)
        self.stateTooltip = None

        self.revo_btn.setEnabled(False)

    def add_format(self):
        text = self.content_lineedit.toPlainText()
        text += '%尊称%'
        self.content_lineedit.setPlainText(text)

    def send_msg(self):
        self.send_msg_id = []  # 清空撤回消息
        self.stateTooltip = StateToolTip(self.tr('正在群发消息'), self.tr('请耐心等待'), self.window())
        self.stateTooltip.move(self.stateTooltip.getSuitablePos())
        self.stateTooltip.show()

        message = self.content_lineedit.toPlainText()
        for i, contactInfo in enumerate(shared.contactInfos):
            wxid = contactInfo['wxid']
            massive = shared.contactConfigs[wxid]['massive']
            if massive:
                if '%尊称%' in message:
                    respect = shared.contactConfigs[wxid]['respect']
                    message = message.replace('%尊称%', respect)

                self.wcf.send_text(message, wxid)
                sql = f"SELECT MsgSvrID FROM MSG WHERE StrContent = '{message}'"
                time.sleep(0.5)
                msg_id = self.wcf.query_sql('MSG0.db', sql=sql)
                for msgid in msg_id:
                    m_id = msgid['MsgSvrID']
                    if m_id not in self.send_msg_id:
                        self.send_msg_id.append(m_id)
        print(self.send_msg_id)

        # 完成
        self.stateTooltip.setContent(self.tr('全部发送完成') + ' 😆')
        self.stateTooltip.setState(True)
        self.stateTooltip = None

        self.revo_btn.setEnabled(True)

    def show_option_changed(self, button):
        """显示选项变更"""
        self.show_option_ID = button.group().checkedId()
        self.search_without_params()

    def search_without_params(self):
        self.search(self.searchLineEdit.text())


    def save_contact_config(self):
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(shared.contactConfigs, file, ensure_ascii=False, indent=4)

    def load_contact_config(self):
        with open('data.json', 'r', encoding='utf-8') as file:
            shared.contactConfigs = json.load(file)

    def build_save_dict(self):
        # {"wxid_000":{"respect": "", "massive": False}}
        for i, contactInfo in enumerate(shared.contactInfos):
            if contactInfo['wxid'] not in shared.contactConfigs:
                shared.contactConfigs[contactInfo['wxid']] = {
                    'respect': '',
                    'massive': False
                }

    def set_row_hidden(self, i, contactInfo):
        """设置行显示"""
        wxid = contactInfo['wxid']
        massive = shared.contactConfigs[wxid]['massive']
        if self.show_option_ID == 0:
            self.contactTable.tableView.setRowHidden(i, False)
        elif self.show_option_ID == 1:
            self.contactTable.tableView.setRowHidden(i, not massive)
        else:
            self.contactTable.tableView.setRowHidden(i, massive)

    def search(self, keyWord: str):
        """ 搜索联系人 """
        for i, contactInfo in enumerate(shared.contactInfos):
            wxid = contactInfo['wxid']
            respect = shared.contactConfigs[wxid]['respect']
            if keyWord not in contactInfo['name'] and keyWord not in contactInfo['remark'] and keyWord not in respect:
                self.contactTable.tableView.setRowHidden(i, True)
            else:
                self.set_row_hidden(i, contactInfo)

    def showAll(self):
        """显示所有"""
        for i, contactInfo in enumerate(shared.contactInfos):
            self.set_row_hidden(i, contactInfo)

class SLineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('搜索联系人'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)

class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        # self.setSortingEnabled(True)
        self.top_index = 0

        self.contactInfos = {}
        self.contactConfig = {}

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels([
            self.tr('微信昵称'), self.tr('微信备注'), self.tr('尊称'), self.tr('群发')
        ])

        scroll_bar = self.verticalScrollBar()
        scroll_bar.valueChanged.connect(self.scroll_bar_changed)

        self.itemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        """尊称改变时触发"""
        if item is not None and item.column() == 2:
            row = item.row()
            wxid = shared.contactInfos[row]['wxid']
            shared.contactConfigs[wxid]['respect'] = item.text()
            button = self.cellWidget(row, 3)
            if button is not None:
                button.setEnabled(item.text() != '')

    def buttonSwitched(self, r, state):
        """切换按钮时触发"""
        wxid = shared.contactInfos[r]['wxid']
        shared.contactConfigs[wxid]['massive'] = state
        self.parent.count_mass_user()
        self.parent.parent.search_without_params()

    def scroll_bar_changed(self, value):
        """滚动条滚动时触发"""
        pass


    def refresh_table(self):
        self.clearContents()  # 全部清理

        self.setRowCount(len(shared.contactInfos))

        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        for i, contactInfo in enumerate(shared.contactInfos):
            name_item = QTableWidgetItem(contactInfo["name"])
            name_item.setFlags(name_item.flags() & ~Qt.ItemIsEditable)
            remark_item = QTableWidgetItem(contactInfo["remark"])
            remark_item.setFlags(remark_item.flags() & ~Qt.ItemIsEditable)

            self.setItem(i, 0, name_item)
            self.setItem(i, 1, remark_item)

            respect_text = shared.contactConfigs[contactInfo['wxid']]['respect']
            tmp_item = QTableWidgetItem(respect_text)
            self.setItem(i, 2, tmp_item)

            massive = shared.contactConfigs[contactInfo['wxid']]['massive']
            send_switch = SwitchButton()
            send_switch.setChecked(massive)  # 设置值
            send_switch.setEnabled(respect_text != '')  # 设置是否启用
            send_switch.checkedChanged.connect(lambda state, r=i: self.buttonSwitched(r, state))
            self.setCellWidget(i, 3, send_switch)

        # self.setFixedSize(625, 440)
        self.resizeColumnsToContents()

    def addWidgetItem(self, widget: QWidget):
        tmp_widget = QWidget()
        tmp_layout = QHBoxLayout()
        tmp_layout.addSpacing(20)
        tmp_layout.addWidget(widget)
        tmp_layout.addSpacing(20)
        tmp_widget.setLayout(tmp_layout)
        return tmp_widget


class RadioWidget(QWidget):
    def __init__(self, radios, selected=0, parent=None):
        super().__init__(parent)
        # radio button
        radioLayout = QVBoxLayout(self)
        radioLayout.setContentsMargins(2, 0, 0, 0)
        radioLayout.setSpacing(15)
        self.buttonGroup = QButtonGroup(self)
        for i, radio in enumerate(radios):
            radio_btn = RadioButton(self.tr(radio), self)
            self.buttonGroup.addButton(radio_btn, i)
            radioLayout.addWidget(radio_btn)

        radioLayout.itemAt(selected).widget().click()

class ContactTable(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.parent = parent

        self.blockSignals(True)

        self.tableView = TableFrame(self)
        self.tableView.refresh_table()
        self.controlPanel = QFrame(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        # self.show_check = CheckBox(self.tr('只显示已有尊称的联系人'))

        self.show_option = RadioWidget(radios=['显示全部', '只显示群发', '只显示未群发'])

        self.send_all_data = BodyLabel()


        self.set_all_mass_btn = PrimaryPushButton(self.tr('一键设置群发'))
        self.set_mass_btn = PrimaryPushButton(self.tr('设置群发'))
        self.not_mass_btn = PushButton(self.tr('取消群发'))
        self.not_all_mass_btn = PushButton(self.tr('取消所有群发'))

        # add items to pivot
        self.__initWidget()

        self.set_all_mass_btn.clicked.connect(self.set_all_mass)
        self.not_all_mass_btn.clicked.connect(self.cancel_all_mass)

        self.count_mass_user()
        self.blockSignals(False)

    def count_mass_user(self):
        count = 0
        for contactInfo in shared.contactInfos:
            wxid = contactInfo['wxid']
            massive = shared.contactConfigs[wxid]['massive']
            if massive:
                count += 1
        self.send_all_data.setText(self.tr(f"{count}人已设置群发"))


    def set_all_mass(self):
        """全部群发"""
        for i, contactInfo in enumerate(shared.contactInfos):
            wxid = contactInfo['wxid']
            if shared.contactConfigs[wxid]['respect'] != '':
                self.tableView.cellWidget(i, 3).setChecked(True)
        self.parent.search(self.parent.searchLineEdit.text())
        self.count_mass_user()

    def cancel_all_mass(self):
        """取消全部群发"""
        for i, contactInfo in enumerate(shared.contactInfos):
            wxid = contactInfo['wxid']
            if shared.contactConfigs[wxid]['respect'] != '':
                self.tableView.cellWidget(i, 3).setChecked(False)
        self.parent.search(self.parent.searchLineEdit.text())
        self.count_mass_user()

    def __initWidget(self):
        self.initLayout()

        # self.controlPanel.setObjectName('controlPanel')
        # StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.controlPanel.setObjectName('iconView')
        # self.scrollWidget.setObjectName('scrollWidget')

        StyleSheet.ICON_INTERFACE.apply(self)
        # StyleSheet.ICON_INTERFACE.apply(self.scrollWidget)

        self.connectSignalToSlot()

    def connectSignalToSlot(self):
        pass

    def initLayout(self):

        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tableView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)


        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        # self.panelLayout.addWidget(self.show_check)
        # self.panelLayout.addSpacing(20)
        self.panelLayout.addWidget(self.send_all_data)
        self.panelLayout.addSpacing(20)
        self.panelLayout.addWidget(self.show_option)

        # self.panelLayout.addWidget(self.set_all_mass_btn)
        # self.panelLayout.addWidget(self.not_all_mass_btn)




        self.panelLayout.addStretch()
        self.panelLayout.addWidget(self.set_all_mass_btn)
        self.panelLayout.addWidget(self.not_all_mass_btn)
        # self.panelLayout.addWidget(self.set_mass_btn)
        # self.panelLayout.addWidget(self.not_mass_btn)
