#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import resources.system_resources

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from coda.image_button import *
from coda.toggle_button import *
from coda.tool_tip import *
from coda.select_button import *
from coda.fader import *
from coda.fader_widget import *
from coda.letter_print import *
from coda.effect import *
from coda.mask import *
from coda.background import *
from coda.background_music import *
from coda.portrait import *
from coda.script_parser import *
from coda.sound import *
from coda.voice import *
from coda.data import *
from coda.log import *

class GameEngine(QMainWindow):
    '''this class creates game engine layout and functions'''

    def __init__(self):
        super().__init__()

        self.pixel_ratio = QWindow().devicePixelRatio()

    def create_game_engine_layout(self):

        #set game status
        self.init_status = True
        self.effect_status = False
        self.load_status = False
        self.auto_status = False

        #set QWidget class
        self.game_engine_widget = QWidget()
        self.base_widget = QWidget(self.game_engine_widget)
        self.portrait_widget = QWidget(self.game_engine_widget)
        self.basic_widget = QWidget(self.game_engine_widget)
        self.select_widget = QWidget(self.game_engine_widget)
        self.text_box_widget = QWidget(self.game_engine_widget)
        self.menu_widget = QWidget(self.game_engine_widget)
        self.log_widget = QWidget(self.game_engine_widget)

        #setup base widget
        self.base_widget.setGeometry(0, 0, 1024, 576)
        self.base_widget.setStyleSheet(
                'QWidget { background-color: black; }')

        #create base layout
        #create background label
        self.background = Background(self.base_widget)

        #creaate portrait layout
        #create portrait
        self.portrait = {}
        for i in range(5):
            self.portrait[i] = Portrait(self.portrait_widget)

        #create basic layout
        #create mask label
        self.mask_label = Mask(self.basic_widget)

        #create disable hide label to show all widget
        self.disable_hide_label = QLabel(self.basic_widget)
        self.disable_hide_label.setGeometry(0, 0, 1024, 576)
        self.disable_hide_label.mousePressEvent = self._show_widget

        #create effect label
        self.effect = Effect(self.basic_widget)

        #create select layout
        #create select label
        self.select_background_pixmap = QPixmap(':/sys/select_background.png')
        self.select_background_pixmap = self.select_background_pixmap.scaledToHeight(
                self.select_background_pixmap.height() * self.pixel_ratio / 2,
                Qt.SmoothTransformation)
        self.select_background_pixmap.setDevicePixelRatio(self.pixel_ratio)
        self.select_background_label = QLabel(self.select_widget)
        self.select_background_label.setPixmap(self.select_background_pixmap)
        self.select_background_label.setGeometry(0, 0, 1024, 576)

        #create selection button
        self.selection_button = {}

        #create text box layout
        #create text background label
        self.text_background_pixmap = QPixmap(':/sys/text_background.png')
        self.text_background_pixmap = self.text_background_pixmap.scaledToHeight(
                self.text_background_pixmap.height() * self.pixel_ratio / 2,
                Qt.SmoothTransformation)
        self.text_background_pixmap.setDevicePixelRatio(self.pixel_ratio)
        self.text_background_label = QLabel(self.text_box_widget)
        self.text_background_label.setPixmap(self.text_background_pixmap)
        self.text_background_label.setGeometry(0, 396, 1024, 180)

        #set the text character label
        self.text_character_label = QLabel(self.text_box_widget)
        self.text_character_label.setAlignment(Qt.AlignLeft)
        self.text_character_label.setGeometry(130, 436, 710, 30)
        self.text_character_label.setFont(QFont('Times New Roman', 23, QFont.Bold))

        #set the text box label
        self.text_box_label = LetterPrint(self.text_box_widget)
        self.text_box_label.setAlignment(Qt.AlignLeft)
        self.text_box_label.setGeometry(140, 476, 700, 75)
        self.text_box_label.setWordWrap(True)
        self.text_box_label.setFont(QFont('Times New Roman', 21))

        #create transparent label to add game engine id(next)
        self.next_label = QLabel(self.text_box_widget)
        self.next_label.setGeometry(0, 0, 1024, 576)
        self.next_label.mousePressEvent = self._update_engine

        #create a auto button
        self.auto_tool_tip = ToolTip('auto', self.text_box_widget)
        self.auto_tool_tip.setGeometry(894, 456, 85, 25)
        self.auto_tool_tip.setVisible(False)
        self.auto_active_tool_tip = ToolTip('auto_active', self.text_box_widget)
        self.auto_active_tool_tip.setGeometry(894, 456, 85, 25)
        self.auto_active_tool_tip.hide()
        self.auto_button = ToggleButton('auto', self.text_box_widget)
        self.auto_button.setGeometry(874, 486, 35, 35)
        self.auto_button.clicked.connect(self._change_auto_status)
        self.auto_button.mouse_hover.connect(self.auto_tool_tip.setVisible)

        #create a skip button
        self.skip_tool_tip = ToolTip('skip', self.text_box_widget)
        self.skip_tool_tip.setGeometry(894, 456, 85, 25)
        self.skip_tool_tip.setVisible(False)
        self.skip_active_tool_tip = ToolTip('skip_active', self.text_box_widget)
        self.skip_active_tool_tip.setGeometry(894, 456, 85, 25)
        self.skip_active_tool_tip.hide()
        self.skip_button = ImageButton('skip', self.text_box_widget)
        self.skip_button.setGeometry(919, 486, 35, 35)
        self.skip_button.mousePressEvent = self._skip
        self.skip_button.mouseReleaseEvent = self._disable_skip
        self.skip_button.mouse_hover.connect(self.skip_tool_tip.setVisible)

        #create a log button
        self.log_tool_tip = ToolTip('log', self.text_box_widget)
        self.log_tool_tip.setGeometry(894, 456, 85, 25)
        self.log_tool_tip.setVisible(False)
        self.log_button = ImageButton('log', self.text_box_widget)
        self.log_button.setGeometry(964, 486, 35, 35)
        self.log_button.clicked.connect(self._show_log)
        self.log_button.mouse_hover.connect(self.log_tool_tip.setVisible)

        #create a save button
        self.save_tool_tip = ToolTip('save', self.text_box_widget)
        self.save_tool_tip.setGeometry(894, 456, 85, 25)
        self.save_tool_tip.setVisible(False)
        self.save_button = ImageButton('save', self.text_box_widget)
        self.save_button.setGeometry(874, 531, 35, 35)
        self.save_button.clicked.connect(self._save_data)
        self.save_button.mouse_hover.connect(self.save_tool_tip.setVisible)

        #create a load button
        self.load_tool_tip = ToolTip('load', self.text_box_widget)
        self.load_tool_tip.setGeometry(894, 456, 85, 25)
        self.load_tool_tip.setVisible(False)
        self.load_button = ImageButton('load', self.text_box_widget)
        self.load_button.setGeometry(919, 531, 35, 35)
        self.load_button.clicked.connect(self._disable_auto_status)
        self.load_button.mouse_hover.connect(self.load_tool_tip.setVisible)

        #create a menu button
        self.menu_tool_tip = ToolTip('menu', self.text_box_widget)
        self.menu_tool_tip.setGeometry(894, 456, 85, 25)
        self.menu_tool_tip.setVisible(False)
        self.menu_button = ImageButton('menu', self.text_box_widget)
        self.menu_button.setGeometry(964, 531, 35, 35)
        self.menu_button.clicked.connect(self._show_menu)
        self.menu_button.mouse_hover.connect(self.menu_tool_tip.setVisible)

        #create a hide button
        self.hide_button = ImageButton('hide', self.text_box_widget)
        self.hide_button.setGeometry(839, 456, 25, 25)
        self.hide_button.clicked.connect(self._hide_widget)

        #create menu layout
        #create menu background
        self.menu_background_pixmap = QPixmap(':/sys/menu_background.png')
        self.menu_background_pixmap = self.menu_background_pixmap.scaledToHeight(
                self.menu_background_pixmap.height() * self.pixel_ratio / 2,
                Qt.SmoothTransformation)
        self.menu_background_pixmap.setDevicePixelRatio(self.pixel_ratio)
        self.menu_background_label = QLabel(self.menu_widget)
        self.menu_background_label.setPixmap(self.menu_background_pixmap)
        self.menu_background_label.setGeometry(0, 0, 1024, 576)

        #create log layout
        self.log = Log(self.log_widget)
        self.log.log_back_button.clicked.connect(self._hide_log)

        #create back button
        self.back_button = ImageButton('menu_back', self.menu_widget)
        self.back_button.setGeometry(60, 275, 96, 32)
        self.back_button.clicked.connect(self._hide_menu)

        #create title button
        self.title_button = ImageButton('menu_title', self.menu_widget)
        self.title_button.setGeometry(290, 275, 96, 32)

        #create config button
        self.config_button = ImageButton('menu_config', self.menu_widget)
        self.config_button.setGeometry(520, 275, 96, 32)

        #create exit button
        self.exit_button = ImageButton('menu_quit', self.menu_widget)
        self.exit_button.setGeometry(750, 275, 96, 32)

        #hide widget
        self.log_widget.hide()
        self.menu_widget.hide()
        self.text_box_widget.hide()
        self.select_widget.hide()
        self.disable_hide_label.hide()
        self.effect.hide()

        #set media
        self.voice = Voice()
        self.voice.stateChanged.connect(self._voice_standby)
        self.background_music = {}
        self.sound = {}
        for i in range(2):
            self.background_music[i] = BackgroundMusic()
        for i in range(3):
            self.sound[i] = Sound()

        #set parser
        self.parser = ScriptParser()

        #set data 
        self.data = Data()
        self.save_data = Data()

        #set save thumbnail
        self.thumbnail = QPixmap(2048, 1152)
        self.thumbnail = self.thumbnail.scaledToHeight(
                self.thumbnail.height() * self.pixel_ratio / 2,
                Qt.SmoothTransformation)
        self.thumbnail.setDevicePixelRatio(self.pixel_ratio)

        #set timer
        self.text_timer = QTimer()
        self.text_timer.setSingleShot(True)
        self.text_timer.timeout.connect(self._auto_emit)
        self.voice_timer = QTimer()
        self.voice_timer.setSingleShot(True)
        self.voice_timer.timeout.connect(self._auto_emit)
        self.auto_timer = QTimer()
        self.auto_timer.setSingleShot(True)
        self.auto_timer.timeout.connect(self._auto_emit)
        self.text_box_label.next_timer.timeout.connect(self._text_standby)

    ############################## MAIN PROGRAM START ##############################

    def start_game(self, script, game_engine_id):

        self.script = script
        self.game_engine_id = game_engine_id
        self.init_status = True
        self.log.add_log('', '< ゲームを始めます >', 1)
        self._init_parser()

    def load_game(self, load_data):

        self.load_data = load_data
        self.script = self.load_data.sys_ldsc
        self.game_engine_id = int(self.load_data.sys_ldid)
        self.init_status = True
        self.load_status = True
        self.log.add_log('', '< ゲームを読みます >', 1)
        self._init_parser()

    def _init_parser(self):

        #print('init_parser')

        if self.load_status == True:
            self.parser.data = copy.deepcopy(self.load_data)
        else:
            self.parser.parse(self.script, self.game_engine_id)

        self.data = copy.deepcopy(self.parser.data)

        if self.data.sys_sc != '':
            self.script = self.data.sys_sc
            self.game_engine_id = -1
        if self.data.sl_num != 0:
            self._selection()
        else:
            if self.init_status:
                self.data.eff_id = 'black_fade'
                self.data.eff_du = '2000'
                self.data.tb_sh = True
                if self.data.tb_td == '':
                    self.data.tb_td = 1000
                self._pre_process()
            self._init_background_music()

    def _init_background_music(self):

        #print('init_background_music')

        if self.load_status == True:
            QTimer.singleShot(1250, self._delay_init_background_music)

        else:
            self.background.show()
            if self.data.bgm_num != 0:
                self._pre_bgm_loop()

            self._init_effect()

    def _init_effect(self):

        #print('init_effect')

        if self.data.eff_id != '':

            self.background.anime.stop()
            self.next_label.hide()

            if not self.init_status:
                self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
                self.fader.fade(800)

            self.effect.show()
            self.effect.create(self.data.eff_id)
            QTimer.singleShot(int(self.data.eff_du), self._hide_effect)

        else:
            self.effect_status = False
            self._init_sound()
        
        self.init_status = False

    def _init_sound(self):

        #print('init_sound')

        if self.data.sd_num != 0:
            self._pre_sd_loop()

        self._init_mask()

    def _init_mask(self):

        #print('init_mask')

        if self.data.mk_md == 'new':
            self.mask_label.set_mask(self.data.mk_id)
        elif self.data.mk_md == 'del':
            self.mask_label.delete_mask()

        self._init_background()

    def _init_background(self):

        #print('init_background')

        if self.data.bg_id != '':

            if not self.effect_status:
                self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
                self.fader.fade(800)

            if self.data.bg_du != '':
                if self.data.eff_du == '' and self.data.tb_sh != '':
                    self._pre_process()
                self.background.create_mv_bg(self.data.bg_id,
                        int(self.data.bg_x), int(self.data.bg_y),
                        int(self.data.bg_xf), int(self.data.bg_yf),
                        int(self.data.bg_du))
            else:
                if self.data.bg_x == '':
                    self.data.bg_x = 0
                if self.data.bg_y == '':
                    self.data.bg_y = 0
                self.background.create_bg(self.data.bg_id,
                        int(self.data.bg_x), int(self.data.bg_y))

        self._init_portrait()

    def _init_portrait(self):

        #print('init_portrait')

        if self.data.pt_num != 0:
            self._pre_pt_loop()

        self._init_text_box()

    def _init_text_box(self):

        #print('init_text_box')

        self.text_character_label.clear()
        self.text_box_label.clear()

        if self.data.tb_sh != '':
            self._show_text_box()

        else:
            self._init_voice()

    def _init_voice(self):

        #print('init_voice')

        if self.data.tb_vc != '':
            self.voice.play_voice(self.data.tb_vc)

        self._init_text()

    def _init_text(self):

        #print('init_text')

        self.text_character_label.setText(self.data.tb_char)
        self.text_box_label.set_verbatim_text(self.data.tb_txt)

        self.log.add_log(self.data.tb_char, self.data.tb_txt, 0)

    def _update_engine(self, event):

        if self.text_box_label.index < len(self.data.tb_txt):
            self.text_box_label.setText(self.data.tb_txt)
            self.text_box_label.index = len(self.data.tb_txt)

        else:
            self._update()

    def _update(self):

        self.game_engine_id += 1
        self._set_background_music()

    def _set_background_music(self):

        #print('set_background_music')

        if self.data.bgm_num != 0:
            self._post_bgm_loop()

        self._set_sound()

    def _set_sound(self):

        #print('set_sound')

        if self.data.sd_num != 0:
            self._post_sd_loop()

        self._set_text()

    def _set_text(self):

        #print('set_text')

        self.text_character_label.clear()
        self.text_box_label.clear()

        self._set_portrait()

    def _set_portrait(self):

        #print('set_portrait')

        if self.data.pt_num != 0:
            self._post_pt_loop()

        self._set_text_box()

    def _set_text_box(self):

        #print('set_text_box')

        if self.data.tb_hi != '':
            self._hide_text_box()

        else:
            self._init_parser()

    ############################## MAIN PROGRAM END ##############################

    #utilities
    def _skip(self, event):

        self._disable_auto_status()
        self.skip_active_tool_tip.show()

    def _disable_skip(self, event):

        self.skip_active_tool_tip.hide()

    def _show_log(self):

        self._disable_auto_status()

        self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
        self.fader.fade(250)
        self.log.set_scroll_position()
        self.log_widget.show()
        self.text_box_widget.hide()

    def _hide_log(self):

        self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
        self.fader.fade(250)
        self.log_widget.hide()
        self.text_box_widget.show()

    def _text_standby(self):

        if (self.data.tb_vc == '' and self.data.tb_txt != ''
                and self.auto_status == True):
            self.text_timer.start(2500)

    def _voice_standby(self):

        if self.voice.state() == 0 and self.auto_status == True:
            self.voice_timer.start(250)

    def _change_auto_status(self):

        if self.auto_status == False:
            self.auto_status = True
            self.next_label.setEnabled(False)
            self.hide_button.hide()
            self.auto_active_tool_tip.show()
            if (self.voice.state() == 0
                    and self.text_box_label.index >= len(self.data.tb_txt)):
                self.text_timer.stop()
                self.voice_timer.stop()
                self.auto_timer.stop()
                self.auto_timer.start(1000)
        else:
            self._disable_auto_status()

    def _disable_auto_status(self):

        self.auto_status = False
        self.auto_button.state = 0
        self.next_label.setEnabled(True)
        self.hide_button.show()
        self.auto_active_tool_tip.hide()

    def _auto_emit(self):

        if self.auto_status == True:
            self._update()

    def _hide_menu(self):

        self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
        self.fader.fade(250)
        self.menu_widget.hide()
        self.text_box_widget.show()

    def _show_menu(self):

        self._disable_auto_status()

        self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
        self.fader.fade(250)
        self.menu_widget.show()
        self.text_box_widget.hide()

    def _hide_widget(self):

        self.hide_button.setEnabled(False)
        self.next_label.hide()
        self.fader_widget = FaderWidget(self.text_box_widget, 1.0)
        self.fader_widget.hide(250)
        self.fader_widget.anime.finished.connect(self._finish_hide_widget)

    def _finish_hide_widget(self):

        self.text_box_widget.hide()
        self.disable_hide_label.show()

    def _show_widget(self, event):

        self.text_box_widget.show()
        self.fader_widget = FaderWidget(self.text_box_widget, 0.0)
        self.fader_widget.show(250)
        self.fader_widget.anime.finished.connect(self._finish_show_widget)

    def _finish_show_widget(self):

        self.disable_hide_label.hide()
        self.next_label.show()
        self.hide_button.setEnabled(True)

    def _delay_init_background_music(self):

        self.load_status = False
        self._init_background_music()

    def _hide_effect(self):

        self.effect_status = True
        self.next_label.show()
        self.text_box_label.clear()
        self.text_character_label.clear()

        self.fader = Fader(self.game_engine_widget, self.game_engine_widget)
        self.fader.fade(800)

        self.effect.hide()
        self._init_sound()

    def _show_text_box(self):

        self.next_label.hide()
        self.hide_button.setEnabled(False)

        if self.data.tb_td != '':
            QTimer.singleShot(int(self.data.tb_td), self._delay_show_text_box)

        else:
            self.text_box_widget.show()
            self.fader_widget = FaderWidget(self.text_box_widget, 0.0)
            self.fader_widget.show(400)
            self.fader_widget.anime.finished.connect(self._finish_show_text_box)

    def _delay_show_text_box(self):

        self.text_box_widget.show()
        self.fader_widget = FaderWidget(self.text_box_widget, 0.0)
        self.fader_widget.show(400)
        self.fader_widget.anime.finished.connect(self._finish_show_text_box)

    def _finish_show_text_box(self):

        self.disable_hide_label.hide()
        self.next_label.show()
        self.hide_button.setEnabled(True)
        self._init_voice()

    def _hide_text_box(self):

        self.next_label.hide()
        self.disable_hide_label.hide()
        self.hide_button.setEnabled(False)
        self.fader_widget = FaderWidget(self.text_box_widget, 1.0)
        self.fader_widget.hide(400)
        self.fader_widget.anime.finished.connect(self._finsh_hide_text_box)

    def _finsh_hide_text_box(self):

        self.next_label.show()
        self.text_box_widget.hide()
        self._init_parser()

    def _pre_process(self):

        self.pre_effect = QGraphicsOpacityEffect()
        self.pre_effect.setOpacity(0.000001)
        self.text_box_widget.setGraphicsEffect(self.pre_effect)
        self.text_box_widget.show()
        self.text_box_label.setText('     ')

    #main program functions
    def _selection(self):

        #print('selection')

        for i in range(self.data.sl_num):

            pos = 250 + int(i - int(self.data.sl_num / 2)) * 75

            self.selection_button[i] = SelectButton(self.select_widget)
            self.selection_button[i].setStyleSheet(
                    'QAbstractButton { font-family: Times New Roman;\
                    font-size: 21px; }')
            self.selection_button[i].id = '{0}'.format(i)
            self.selection_button[i].set_text(self.data.sl_txt[i])
            self.selection_button[i].setGeometry(0, pos, 1024, 65)
            self.selection_button[i].clicked.connect(self._jump_script)

        fader = Fader(self.game_engine_widget, self.game_engine_widget)
        fader.fade(800)
        self.select_widget.show()

    def _jump_script(self):

        selection = int(self.sender().id)
        #print(selection)
        self.log.add_log('', '< 選択 >    {0}'.format(self.data.sl_txt[selection]), 1)

        self.game_engine_id = 0
        self.script = self.data.sl_sc[selection]
        #print(self.script)

        fader = Fader(self.game_engine_widget, self.game_engine_widget)
        fader.fade(800)
        self.select_widget.hide()
        for each in self.selection_button:
            self.selection_button[each].deleteLater()
        self.selection_button.clear()
        self._init_parser()

    def _pre_bgm_loop(self):

        for i in range(self.data.bgm_num):

            if self.data.bgm_md[i] == 'new':
                self.background_music[
                        int(self.data.bgm_pos[i])].play_music(
                                self.data.bgm_id[i])
            elif self.data.bgm_md[i] == 'vol':
                self.background_music[
                        int(self.data.bgm_pos[i])].music_volume(
                                int(self.data.bgm_vol[i]))
            elif self.data.bgm_md[i] == 'del':
                self.background_music[
                        int(self.data.bgm_pos[i])].stop_music()

    def _post_bgm_loop(self):

        for i in range(self.data.bgm_num):

            if self.data.bgm_md[i] == 'dell':
                self.background_music[int(self.data.bgm_pos[i])].stop_music()

    def _pre_pt_loop(self):

        for i in range(self.data.pt_num):

            if self.data.pt_md[i] == 'new':
                if self.data.pt_du.get(i) != None:
                    self.portrait[int(self.data.pt_pos[i])].create_mv_pt(
                            self.data.pt_id[i],
                            int(self.data.pt_x[i]), int(self.data.pt_y[i]),
                            int(self.data.pt_xf[i]), int(self.data.pt_yf[i]),
                            int(self.data.pt_du[i]))
                else:
                    self.portrait[int(self.data.pt_pos[i])].create_pt(
                            self.data.pt_id[i],
                            int(self.data.pt_x[i]), int(self.data.pt_y[i]))

            elif self.data.pt_md[i] == 'mv':
                self.portrait[int(self.data.pt_pos[i])].move_pt(
                        int(self.data.pt_xf[i]),
                        int(self.data.pt_yf[i]), int(self.data.pt_du[i]))

            elif self.data.pt_md[i] == 'del':
                if self.data.pt_du.get(i) != None:
                    self.portrait[int(self.data.pt_pos[i])].delete_mv_pt(
                            int(self.data.pt_xf[i]), int(self.data.pt_yf[i]),
                            int(self.data.pt_du[i]))
                else:
                    self.portrait[int(self.data.pt_pos[i])].delete_pt()

    def _post_pt_loop(self):

        for i in range(self.data.pt_num):

            if self.data.pt_md[i] == 'dell':
                if self.data.pt_du.get(i) != None:
                    self.portrait[int(self.data.pt_pos[i])].delete_mv_pt(
                            int(self.data.pt_xf[i]), int(self.data.pt_yf[i]),
                            int(self.data.pt_du[i]))
                else:
                    self.portrait[int(self.data.pt_pos[i])].delete_pt()

    def _pre_sd_loop(self):

        for i in range(self.data.sd_num):

            if self.data.sd_md[i] == 'new':
                self.sound[
                        int(self.data.sd_pos[i])].play_sound(self.data.sd_id[i],
                                self.data.sd_lp.get(i), self.data.sd_fd.get(i))
            elif self.data.sd_md[i] == 'del':
                self.sound[
                        int(self.data.sd_pos[i])].stop_sound(self.data.sd_dfd.get(i))

    def _post_sd_loop(self):

        for i in range(self.data.sd_num):

            if self.data.sd_md[i] == 'newl':
                self.sound[
                        int(self.data.sd_pos[i])].play_sound(self.data.sd_id[i],
                                self.data.sd_lp.get(i), self.data.sd_fd.get(i))
            if self.data.sd_md[i] == 'dell':
                self.sound[
                        int(self.data.sd_pos[i])].stop_sound(self.data.sd_dfd.get(i))

    def _save_data(self):

        self._disable_auto_status()

        self.game_engine_widget.render(self.thumbnail)
        self.save_data = copy.deepcopy(self.parser.data)
        self.save_data.sys_ldsc = self.script
        self.save_data.sys_ldid = self.game_engine_id

        for i in range(2):
            if self.background_music[i].state() == 1:
                dupli = False
                for j in range(self.save_data.bgm_num):
                    if (self.save_data.bgm_pos.get(j) == str(i)
                            and self.save_data.bgm_id.get(j)\
                                    == self.background_music[i].id
                            and self.save_data.bgm_md.get(j) == 'new'):
                        dupli = True
                if dupli == False:
                    self.save_data.bgm_pos[self.save_data.bgm_num] = str(i)
                    self.save_data.bgm_id[self.save_data.bgm_num]\
                            = self.background_music[i].id
                    self.save_data.bgm_md[self.save_data.bgm_num] = 'new'
                    self.save_data.bgm_num += 1
                    self.save_data.bgm_pos[self.save_data.bgm_num] = str(i)
                    self.save_data.bgm_vol[self.save_data.bgm_num]\
                            = self.background_music[i].volume()
                    self.save_data.bgm_md[self.save_data.bgm_num] = 'vol'
                    self.save_data.bgm_num += 1

        for i in range(3):
            if (self.sound[i].state() == 1
                    and self.sound[i].playlist.playbackMode() == 3):
                dupli = False
                for j in range(self.save_data.sd_num):
                    if (self.save_data.sd_pos.get(j) == str(i)
                            and self.save_data.sd_id.get(j)\
                                    == self.sound[i].id
                            and self.save_data.sd_lp.get(j) != None):
                        dupli = True
                if dupli == False:
                    self.save_data.sd_pos[self.save_data.sd_num] = str(i)
                    self.save_data.sd_id[self.save_data.sd_num]\
                            = self.sound[i].id
                    self.save_data.sd_md[self.save_data.sd_num] = 'new'
                    self.save_data.sd_lp[self.save_data.sd_num] = 'True'
                    self.save_data.sd_fd[self.save_data.sd_num] = 'True'
                    self.save_data.sd_num += 1

        if (self.mask_label.id != ''
                and self.save_data.mk_id != self.mask_label.id
                and self.save_data.mk_md != 'new'):
            self.save_data.mk_id = self.mask_label.id
            self.save_data.mk_md = 'new'

        self.save_data.bg_id = self.background.id
        self.save_data.bg_x = int(self.background.x)
        self.save_data.bg_y = int(self.background.y)
        self.save_data.bg_xf = ''
        self.save_data.bg_yf = ''
        self.save_data.bg_du = ''
        print(self.background.duration != 0
                and (int(self.background.x) != self.background.posxf
                or int(self.background.y) != self.background.posyf))
        if (self.background.duration != 0
                and (int(self.background.x) != self.background.posxf
                or int(self.background.y) != self.background.posyf)):
            self.save_data.bg_xf = self.background.posxf
            self.save_data.bg_yf = self.background.posyf
            self.save_data.bg_du = int(self.background.duration\
                    * ((self.background.posxf - self.background.x) ** 2
                    + (self.background.posyf - self.background.y) ** 2)\
                    ** 0.5\
                    / ((self.background.posxf - self.background.posx) ** 2
                    + (self.background.posyf - self.background.posy) ** 2)\
                    ** 0.5)

        for i in range(5):
            if self.portrait[i].opacity != 0:
                dupli = False
                for j in range(self.save_data.pt_num):
                    if (self.save_data.pt_pos.get(j) == str(i)
                            and self.save_data.pt_id.get(j)\
                                    == self.portrait[i].id
                            and self.save_data.pt_md.get(j) == 'new'):
                        dupli = True
                if dupli == False:
                    self.save_data.pt_pos[self.save_data.pt_num] = str(i)
                    self.save_data.pt_id[self.save_data.pt_num]\
                            = self.portrait[i].id
                    self.save_data.pt_md[self.save_data.pt_num] = 'new'
                    self.save_data.pt_x[self.save_data.pt_num]\
                            = int(self.portrait[i].x)
                    self.save_data.pt_y[self.save_data.pt_num]\
                            = int(self.portrait[i].y)
                    self.save_data.pt_num += 1
