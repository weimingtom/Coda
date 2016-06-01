#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from image_button_class import *
from fader_widget_class import *
from letter_print_class import *
from portrait_label_class import *

import sys
import resources

class GameEngine(QMainWindow):
    """this class creates game engine layout and functions"""

    #constructor
    def __init__(self):
        super().__init__() #call super class constructor

    def create_game_engine_layout(self, game_engine_id):
        #this is the layout for the game engine window

        self.game_engine_id = game_engine_id #get the game engine id from positional argument
        print(self.game_engine_id)

        #set QWidget class
        self.game_engine_widget = QWidget()
        self.basic_widget = QWidget(self.game_engine_widget) #widget for basic widget
        self.text_box_widget = QWidget(self.game_engine_widget) #widget for text box widget
        self.log_widget = QWidget(self.game_engine_widget) #widget for log widget
        self.menu_widget = QWidget(self.game_engine_widget) #widget for menu widget

        #create basic game engine layout
        #create background cg
        self.cg = QLabel(self.basic_widget)
        self.cg.setPixmap(QPixmap(":/bg_0000.png"))
        self.cg.setGeometry(0, 0, 960, 540)

        #create portrait label
        self.portrait = Portrait(self.basic_widget)
        self.portrait.show_portrait("aoi_normal", 400, 40, 500, 40, 280, 500)

        #create text background label
        self.text_background_label = QLabel(self.text_box_widget)
        self.text_background_label.setPixmap(QPixmap(":/text_background.png"))
        self.text_background_label.setGeometry(0, 340, 960, 200)

        #set the text box label
        self.text = "Test Text\n測試文本\nテストテキスト"
        self.text_font = QFont("Noto Sans CJK TC Regular", 14, QFont.Bold)
        self.text_box_label = LetterPrint(self.text_box_widget)
        self.text_box_label.set_text(self.text)
        self.text_box_label.setFont(self.text_font)
        self.text_box_label.setAlignment(Qt.AlignLeft) #make text align top left
        self.text_box_label.setGeometry(100, 430, 685, 100)
        self.text_box_label.setStyleSheet("QLabel {color: rgba(255, 255, 255, 100%)}")

        #create disable hide label to show all widget
        self.disable_hide_label = QLabel(self.basic_widget)
        self.disable_hide_label.setGeometry(0, 0, 960, 540)
        self.hide() #hide this widget at first

        #create transparent label to add game engine id(next)
        self.next_label = QLabel(self.text_box_widget)
        self.next_label.setGeometry(0, 0, 960, 540)

        #create a auto button
        self.auto_button = ImageButton("auto", self.text_box_widget)
        self.auto_button.setGeometry(810, 435, 35, 35)

        #create a skip button
        self.skip_button = ImageButton("skip", self.text_box_widget)
        self.skip_button.setGeometry(855, 435, 35, 35)

        #create a log button
        self.log_button = ImageButton("log", self.text_box_widget)
        self.log_button.setGeometry(900, 435, 35, 35)

        #create a save button
        self.save_button = ImageButton("save", self.text_box_widget)
        self.save_button.setGeometry(810, 480, 35, 35)

        #create a load button
        self.load_button = ImageButton("load", self.text_box_widget)
        self.load_button.setGeometry(855, 480, 35, 35)

        #create a menu button
        self.menu_button = ImageButton("menu", self.text_box_widget)
        self.menu_button.setGeometry(900, 480, 35, 35)

        #create a hide button
        self.hide_button = ImageButton("hide", self.text_box_widget)
        self.hide_button.setGeometry(760, 400, 25, 25)

        #create menu layout
        #create menu background
        self.menu_background_label = QLabel(self.menu_widget)
        self.menu_background_label.setPixmap(QPixmap(":/menu_background.png"))
        self.menu_background_label.setGeometry(0, 0, 960, 540)

        #create back button
        self.back_button = ImageButton("menu_back", self.menu_widget)
        self.back_button.setGeometry(400, 64, 160, 55)

        #create title button
        self.title_button = ImageButton("menu_title", self.menu_widget)
        self.title_button.setGeometry(400, 183, 160, 55)

        #create config button
        self.config_button = ImageButton("menu_config", self.menu_widget)
        self.config_button.setGeometry(400, 302, 160, 55)

        #create exit button
        self.exit_button = ImageButton("menu_exit", self.menu_widget)
        self.exit_button.setGeometry(400, 421, 160, 55)

        #hide text box widget
        self.text_box_widget.hide()

        #hide menu widget
        self.menu_widget.hide()

        #connection
        self.back_button.clicked.connect(self.hide_menu)
        self.menu_button.clicked.connect(self.show_menu)
        self.hide_button.clicked.connect(self.hide_widget)
        self.disable_hide_label.mousePressEvent = self.show_widget
        self.next_label.mousePressEvent = self.update

    def hide_menu(self):
        #this is the funtion to hide menu layout

        self.fader_widget = FaderWidget(self.game_engine_widget, self.game_engine_widget) #call fade class
        self.fader_widget.fade(0, 0, 960, 540, 250)
        self.menu_widget.hide()
        self.text_box_widget.show()

    def show_menu(self):
        #this is the funtion to show menu layout

        self.fader_widget = FaderWidget(self.game_engine_widget, self.game_engine_widget) #call fade class
        self.fader_widget.fade(0, 0, 960, 540, 250)
        self.menu_widget.show()
        self.text_box_widget.hide()

    def hide_widget(self):
        #this is the funtion to hide all widgets

        self.fader_widget = FaderWidget(self.game_engine_widget, self.game_engine_widget) #call fade class
        self.fader_widget.fade(0, 0, 960, 540, 250)
        self.text_box_widget.hide()
        self.disable_hide_label.show()

    def show_widget(self, event):
        #this is the funtion to show all widgets

        self.fader_widget = FaderWidget(self.game_engine_widget, self.game_engine_widget) #call fade class
        self.fader_widget.fade(0, 0, 960, 540, 250)
        self.text_box_widget.show()
        self.disable_hide_label.hide()

    def update(self, event):
        #this is the function to update game engine layout

        #check if this text is already shown after label was pressed
        if self.text_box_label.index < len(self.text):
            self.text_box_label.setText(self.text) #if not call setText function
            self.text_box_label.index = len(self.text)

        else:
            self.game_engine_id += 1
            print("update")
            print(self.game_engine_id)

            self.portrait.hide_portrait("aoi_normal")

            self.fader_widget = FaderWidget(self.game_engine_widget, self.game_engine_widget) #call fade class
            self.fader_widget.fade(0, 0, 960, 540, 250)

            self.text = "Hi! This is line {0}".format(self.game_engine_id)
            self.text_box_label.set_text(self.text)