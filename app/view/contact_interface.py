from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, PushSettingCard,
                            HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ComboBoxSettingCard, ExpandLayout, Theme, CustomColorSettingCard,
                            setTheme, setThemeColor, RangeSettingCard, isDarkTheme, HeaderCardWidget, TitleLabel,
                            TableWidget, SearchLineEdit, SwitchButton, RadioButton, StrongBodyLabel, BodyLabel,
                            IconWidget, FluentIcon, PushButton, PrimaryPushButton)
from PySide6.QtCore import Qt, Signal, QUrl, QStandardPaths, QEvent
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QVBoxLayout, QTableWidgetItem, QHBoxLayout, QFrame, \
    QButtonGroup, QTableWidget, QHeaderView
from ..common.style_sheet import StyleSheet
from ..common.translator import Translator
from .gallery_interface import GalleryInterface

class LineEdit(SearchLineEdit):
    """ Search line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setPlaceholderText(self.tr('搜索联系人'))
        self.setFixedWidth(304)
        self.textChanged.connect(self.search)

class ContactInterface(GalleryInterface):
    """ Setting interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=self.tr("联系人"),
            subtitle="管理联系人是否托管",
            parent=parent
        )
        self.setObjectName('contactInterface')

        self.searchLineEdit = LineEdit(self)

        self.vBoxLayout.addWidget(self.searchLineEdit)

        self.contactTable = ContactTable(self)

        self.vBoxLayout.addWidget(self.contactTable)

        self.searchLineEdit.clearSignal.connect(self.showAll)
        self.searchLineEdit.searchSignal.connect(self.search)

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


class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(3)

        self.setHorizontalHeaderLabels([
            self.tr('昵称'), self.tr('备注'), self.tr('是否托管')
        ])

        contactInfos = [
            {'wxid': '25984983094317076@openim', 'code': '', 'remark': '', 'name': '叶凤娟', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982554273028@openim', 'code': '', 'remark': '', 'name': 'P0超站-若汐', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982426268482@openim', 'code': '', 'remark': '', 'name': '首席灯光顾问', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984985113441984@openim', 'code': '', 'remark': '', 'name': '小名同学', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982651696129@openim', 'code': '', 'remark': '', 'name': '龚春林', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984983482227117@openim', 'code': '', 'remark': '', 'name': '商务橘猫', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984981798520676@openim', 'code': '', 'remark': '', 'name': '陈丹彤(今日休息，紧急情况可致电前台02082098860，24小时值班电话02082098986)', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984951827814@openim', 'code': '', 'remark': '', 'name': '中国电信泰安北路营业厅', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982456668711@openim', 'code': '', 'remark': '', 'name': '曹传双', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984983756838188@openim', 'code': '', 'remark': 'UE 店长', 'name': '店长', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984981867692802@openim', 'code': '', 'remark': '', 'name': '商务-黑猫3号', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984420545931@openim', 'code': '', 'remark': '', 'name': '商务-小纯', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984861924011@openim', 'code': '', 'remark': '', 'name': '售前客服-小迅', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984052550353@openim', 'code': '', 'remark': '', 'name': '谢天纯', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984985592591891@openim', 'code': '', 'remark': '', 'name': '杨少锐', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984985647151414@openim', 'code': '', 'remark': '', 'name': '陈思彤', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984983310246809@openim', 'code': '', 'remark': '', 'name': '商务 泡沫', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984945657130@openim', 'code': '', 'remark': '', 'name': '李容露', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982605731618@openim', 'code': '', 'remark': '', 'name': '刘恒飞', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984985526545825@openim', 'code': '', 'remark': '', 'name': '莱恩', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984983163445756@openim', 'code': '', 'remark': '', 'name': '泓蓉', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982250358047@openim', 'code': '', 'remark': '', 'name': '闫斌', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984087148462@openim', 'code': '', 'remark': '', 'name': '商务—小黑', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984830472772@openim', 'code': '', 'remark': '', 'name': '张雨', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984984429991313@openim', 'code': '', 'remark': '', 'name': '高雅', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984982859441350@openim', 'code': '', 'remark': '', 'name': '许轩烨', 'country': '', 'province': '', 'city': '', 'gender': ''},
            {'wxid': '25984983865874323@openim', 'code': '', 'remark': '', 'name': '肖佳', 'country': '', 'province': '', 'city': '', 'gender': ''}
        ]

        self.setRowCount(len(contactInfos))
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)

        for i, contactInfo in enumerate(contactInfos):
            self.setItem(i, 0, QTableWidgetItem(contactInfo["name"]))
            self.setItem(i, 1, QTableWidgetItem(contactInfo["remark"]))
            tmp_widget = QWidget()
            tmp_layout = QHBoxLayout()
            tmp_layout.addSpacing(20)
            tmp_layout.addWidget(SwitchButton())
            tmp_layout.addSpacing(20)
            tmp_widget.setLayout(tmp_layout)
            self.setCellWidget(i, 2, tmp_widget)

        # self.setFixedSize(625, 440)
        self.resizeColumnsToContents()


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

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tableView = TableFrame(self)
        self.controlPanel = QFrame(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.show_option = RadioWidget(radios=['显示全部', '只显示已托管', '只显示未托管'])
        self.all_select_btn = PushButton(self.tr('全选'))
        self.ai_btn = PrimaryPushButton(self.tr('托管'))
        self.not_ai_btn = PushButton(self.tr('取消托管'))

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

        # self.setFixedHeight(600)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tableView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.show_option)
        self.panelLayout.addSpacing(20)
        self.panelLayout.addWidget(self.all_select_btn)
        self.panelLayout.addStretch()
        self.panelLayout.addWidget(self.ai_btn)
        self.panelLayout.addWidget(self.not_ai_btn)
