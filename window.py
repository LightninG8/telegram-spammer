################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################

import sys
import asyncio
from datetime import datetime

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import (QCoreApplication, QPropertyAnimation, QDate, QDateTime, QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt, QEvent)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont, QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter, QPixmap, QRadialGradient)
from PyQt5.QtWidgets import *

# GUI FILE
from GUI.ui_main import Ui_MainWindow
from GUI.ui_log import Ui_log
# IMPORT FUNCTIONS
from ui_functions import *

# IMPORT SENDER
# from sender import Sender

class MainWindow(QMainWindow):
    def __init__(
        self,
        connectSender,
        disconnectSender,
        updateAccount,
        start,
        clearProcessedMessages
      ):
        QMainWindow.__init__(self)
        self.config = json.load(open('config.json'))
        self.connectSender = connectSender
        self.disconnectSender = disconnectSender
        self.updateAccount = updateAccount
        self.start = start
        self.clearProcessedMessages = clearProcessedMessages

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## FORMS
        self.initFormsByConfig()

        # self.loop = asyncio.get_event_loop()
        # self.loop.run_until_complete(self.start())
        ## PAGES
        ########################################################################

    # async def start(self):
        # PAGE 1
        self.ui.btn_page_new.clicked.connect(lambda: UIFunctions.changePage(self, self.ui.page_new, self.ui.btn_page_new))

        self.ui.sender_attachment_file.clicked.connect(lambda: UIFunctions.inputFile(self, 'sender_attacment_file_path', self.ui.label_attachment_file))
        self.ui.sender_contacts_file.clicked.connect(lambda: UIFunctions.inputFile(self,'sender_contacts_file_path', self.ui.label_contacts_file))
        self.ui.sender_message.textChanged.connect(lambda: UIFunctions.saveSenderSettings(self))
        self.ui.sender_attachment_type.currentIndexChanged.connect(lambda: UIFunctions.saveSenderSettings(self))
        self.ui.sender_delay.textChanged.connect(lambda: UIFunctions.saveSenderSettings(self))
        self.ui.sender_messages_count.textChanged.connect(lambda: UIFunctions.saveSenderSettings(self))
        self.ui.sender_unqiue.clicked.connect(lambda: UIFunctions.saveSenderSettings(self))
        self.ui.sender_btn_start.clicked.connect(lambda: UIFunctions.startSender(self))
        self.ui.sender_btn_clear_processed.clicked.connect(lambda: UIFunctions.clearProcessedMessages(self))

        # PAGE 2
        self.ui.btn_page_api_settings.clicked.connect(lambda: UIFunctions.changePage(self, self.ui.page_api_settings, self.ui.btn_page_api_settings))

        self.ui.btn_connect_api.clicked.connect(lambda: UIFunctions.connectApi(self))
        self.ui.btn_disconnect_api.clicked.connect(lambda: UIFunctions.disconnectApi(self))
        self.ui.btn_refresh_api_status.clicked.connect(lambda: UIFunctions.refreshApiStatus(self))


        # PAGE 3
        self.ui.btn_page_account_settings.clicked.connect(lambda: UIFunctions.changePage(self, self.ui.page_account_settings, self.ui.btn_page_account_settings))

        self.ui.account_save_btn.clicked.connect(lambda: UIFunctions.saveAccountSettings(self))
        self.ui.account_avatar_file.clicked.connect(lambda: UIFunctions.inputFile(self,'account_avatar_file', self.ui.account_avatar_label))

        # PAGE 4
        self.ui.btn_page_help.clicked.connect(lambda: UIFunctions.changePage(self, self.ui.page_help, self.ui.btn_page_help))

        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    def initFormsByConfig(self):
        # API Settings 
        self.ui.input_api_id.setText(self.config.get('api_id'))
        self.ui.input_api_hash.setText(self.config.get('api_hash'))
        self.ui.input_api_phone.setText(self.config.get('api_phone'))

        if self.config.get('is_connected'):
          self.ui.api_status_label.setText('Подключено')
        else:
          self.ui.api_status_label.setText('Отключено')
        

        # Sender Settings
        self.ui.sender_message.setPlainText(self.config.get('sender_message'))
        self.ui.sender_attachment_type.setCurrentIndex(self.config.get('sender_attachment_type'))
        self.ui.label_attachment_file.setText(self.config.get('sender_attacment_file_path').split('/')[-1])
        self.ui.label_contacts_file.setText(self.config.get('sender_contacts_file_path').split('/')[-1])
        self.ui.sender_delay.setText(self.config.get('sender_delay'))
        self.ui.sender_messages_count.setText(self.config.get('sender_messages_count'))
        self.ui.sender_unqiue.setChecked(self.config.get('sender_unqiue'))

        # Acount Settings
        self.ui.account_firstname.setText(self.config.get('account_firstname'))
        self.ui.account_lastname.setText(self.config.get('account_lastname'))
        self.ui.account_bio.setPlainText(self.config.get('account_bio'))
        self.ui.account_avatar_label.setText(self.config.get('account_avatar_file').split('/')[-1])

    def update(self):
      self.config = json.load(open('config.json'))

      self.initFormsByConfig()

    def log(self, text):
      now = datetime.now()

      current_time = now.strftime("%H:%M:%S")
      self.ui.textBrowser.insertPlainText(f'[{current_time}] {text} \n')

      print(text)
