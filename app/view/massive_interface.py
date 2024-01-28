from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, HeaderCardWidget, TitleLabel,
                            InfoBar, InfoBarPosition, SearchLineEdit, LineEdit, EditableComboBox, Slider, PushButton,
                            PlainTextEdit,
                            TimePicker, CheckBox, PrimaryPushButton, TableWidget, SwitchButton, RadioButton, BodyLabel,
                            CaptionLabel)
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QFrame, \
    QButtonGroup, QTableWidget, QHeaderView
from ..common.style_sheet import StyleSheet
from qfluentwidgets import FluentIcon as FIF
from .gallery_interface import GalleryInterface
from wcferry import Wcf

class MassiveInterface(GalleryInterface):
    """ massive interface """

    def __init__(self, wcf: Wcf, parent=None):
        super().__init__(
            title=self.tr("群发助手"),
            subtitle="只有设置了尊称的联系人才能设置群发",
            parent=parent
        )
        self.setObjectName('massiveInterface')

        self.vBoxLayout.setSpacing(10)


        self.searchLineEdit = SLineEdit(self)
        self.vBoxLayout.addWidget(self.searchLineEdit)
        self.contactTable = ContactTable(wcf, self)
        self.vBoxLayout.addWidget(self.contactTable)
        self.vBoxLayout.addSpacing(20)

        self.content_lineedit = PlainTextEdit()
        self.content_lineedit.setPlaceholderText(self.tr('要发送的消息内容，例如输入：\n值此佳节，给[尊称]拜年，祝新春快乐！\n\n张总收到的就是：\n值此佳节，给张总拜年，祝新春快乐！\n王总收到的就是：\n值此佳节，给王总拜年，祝新春快乐！'))
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

        # self.timer = QWidget()
        # self.time_picker = TimePicker()
        # self.hLayout = QHBoxLayout(self.timer)
        # self.hLayout.setContentsMargins(0, 0, 0, 0)
        # self.auto_send = CheckBox(self.tr('启用'))
        # self.hLayout.addWidget(self.auto_send)
        # self.hLayout.addSpacing(100)
        # self.hLayout.addWidget(self.time_picker)
        #
        # self.addTitleGroup(title='定时发送', subtitle='到了某个时间自动发送', widget=self.timer, stretch=0)

    def search(self, keyWord: str):
        # """ search icons """
        # items = self.trie.items(keyWord.lower())
        # indexes = {i[1] for i in items}
        # self.flowLayout.removeAllWidgets()
        #
        # for i, card in enumerate(self.cards):
        #     isVisible = i in indexes
        #     card.setVisible(isVisible)
        #     if isVisible:
        #         self.flowLayout.addWidget(card)
        pass

    def showAll(self):
        # self.flowLayout.removeAllWidgets()
        # for card in self.cards:
        #     card.show()
        #     self.flowLayout.addWidget(card)
        pass

class SLineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('搜索联系人'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)

class SwitchButtonLineEdit(LineEdit):
    """ Search line edit """

    def __init__(self, widget: SwitchButton, parent=None):
        super().__init__(parent)
        self.widget = widget
        self.textChanged.connect(self.enable)

    def enable(self, text):
        if text == "":
            self.widget.setChecked(False)
            self.widget.setEnabled(False)
        else:
            self.widget.setEnabled(True)

class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels([
            self.tr('微信昵称'), self.tr('微信备注'), self.tr('尊称'), self.tr('是否群发')
        ])

        scroll_bar = self.verticalScrollBar()
        scroll_bar.valueChanged.connect(self.scroll_bar_changed)

        # contactInfos = [
        #     {'wxid': '25984983094317076@openim', 'code': '', 'remark': '', 'name': '叶凤娟', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982554273028@openim', 'code': '', 'remark': '', 'name': 'P0超站-若汐', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982426268482@openim', 'code': '', 'remark': '', 'name': '首席灯光顾问', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984985113441984@openim', 'code': '', 'remark': '', 'name': '小名同学', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982651696129@openim', 'code': '', 'remark': '', 'name': '龚春林', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984983482227117@openim', 'code': '', 'remark': '', 'name': '商务橘猫', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984981798520676@openim', 'code': '', 'remark': '', 'name': '陈丹彤(今日休息，紧急情况可致电前台02082098860，24小时值班电话02082098986)', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984951827814@openim', 'code': '', 'remark': '', 'name': '中国电信泰安北路营业厅', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982456668711@openim', 'code': '', 'remark': '', 'name': '曹传双', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984983756838188@openim', 'code': '', 'remark': 'UE 店长', 'name': '店长', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984981867692802@openim', 'code': '', 'remark': '', 'name': '商务-黑猫3号', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984420545931@openim', 'code': '', 'remark': '', 'name': '商务-小纯', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984861924011@openim', 'code': '', 'remark': '', 'name': '售前客服-小迅', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984052550353@openim', 'code': '', 'remark': '', 'name': '谢天纯', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984985592591891@openim', 'code': '', 'remark': '', 'name': '杨少锐', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984985647151414@openim', 'code': '', 'remark': '', 'name': '陈思彤', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984983310246809@openim', 'code': '', 'remark': '', 'name': '商务 泡沫', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984945657130@openim', 'code': '', 'remark': '', 'name': '李容露', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982605731618@openim', 'code': '', 'remark': '', 'name': '刘恒飞', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984985526545825@openim', 'code': '', 'remark': '', 'name': '莱恩', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984983163445756@openim', 'code': '', 'remark': '', 'name': '泓蓉', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982250358047@openim', 'code': '', 'remark': '', 'name': '闫斌', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984087148462@openim', 'code': '', 'remark': '', 'name': '商务—小黑', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984830472772@openim', 'code': '', 'remark': '', 'name': '张雨', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984984429991313@openim', 'code': '', 'remark': '', 'name': '高雅', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984982859441350@openim', 'code': '', 'remark': '', 'name': '许轩烨', 'country': '', 'province': '', 'city': '', 'gender': ''},
        #     {'wxid': '25984983865874323@openim', 'code': '', 'remark': '', 'name': '肖佳', 'country': '', 'province': '', 'city': '', 'gender': ''}
        # ]
        #
        # self.setRowCount(len(contactInfos))
        # self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        # self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        #
        # for i, contactInfo in enumerate(contactInfos):
        #     self.setItem(i, 0, QTableWidgetItem(contactInfo["name"]))
        #     self.setItem(i, 1, QTableWidgetItem(contactInfo["remark"]))
        #
        #     send_switch = SwitchButton()
        #     send_switch.setEnabled(False)
        #     mark_lineedit = SwitchButtonLineEdit(send_switch)
        #     lineedit_widget = self.addWidgetItem(mark_lineedit)
        #     switch_widget = self.addWidgetItem(send_switch)
        #
        #     self.setCellWidget(i, 2, lineedit_widget)
        #     self.setCellWidget(i, 3, switch_widget)
        #
        # # self.setFixedSize(625, 440)
        # self.resizeColumnsToContents()

    def scroll_bar_changed(self):
        print('1')

    def refresh_table(self, contactInfos):
        self.setRowCount(len(contactInfos))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)

        for i, contactInfo in enumerate(contactInfos):
            if i > 50:
                break
            self.setItem(i, 0, QTableWidgetItem(contactInfo["name"]))
            self.setItem(i, 1, QTableWidgetItem(contactInfo["remark"]))

            send_switch = SwitchButton()
            send_switch.setEnabled(False)
            mark_lineedit = SwitchButtonLineEdit(send_switch)
            lineedit_widget = self.addWidgetItem(mark_lineedit)
            switch_widget = self.addWidgetItem(send_switch)

            self.setCellWidget(i, 2, lineedit_widget)
            self.setCellWidget(i, 3, switch_widget)

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
        buttonGroup = QButtonGroup(self)
        for radio in radios:
            radio_btn = RadioButton(self.tr(radio), self)
            buttonGroup.addButton(radio_btn)
            radioLayout.addWidget(radio_btn)

        radioLayout.itemAt(selected).widget().click()

class ContactTable(QWidget):
    """ Tab interface """

    def __init__(self, wcf: Wcf, parent=None):
        super().__init__(parent=parent)
        self.send_all_user = 0
        friends = wcf.get_friends()
        print(friends)

        self.tableView = TableFrame(self)
        self.tableView.refresh_table(friends)
        self.controlPanel = QFrame(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        # self.show_check = CheckBox(self.tr('只显示已有尊称的联系人'))

        self.show_option = RadioWidget(radios=['显示全部', '只显示群发', '只显示未群发'])

        self.send_all_data = BodyLabel(self.tr(f"{self.send_all_user}人已设置群发"))

        self.set_all_mass_btn = PrimaryPushButton(self.tr('一键设置群发'))
        self.set_mass_btn = PrimaryPushButton(self.tr('设置群发'))
        self.not_mass_btn = PushButton(self.tr('取消群发'))
        self.not_all_mass_btn = PushButton(self.tr('取消所有群发'))

        # add items to pivot
        self.__initWidget()

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
