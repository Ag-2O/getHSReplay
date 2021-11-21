import os
import requests
import datetime
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import subprocess
import xml.etree.ElementTree as ET
import json

class Game:
    def __init__(self):
        # プレイヤーの初期状態
        self.hero = 0   #ウォリアー:0 ハンター:1
        self.player_health = 30
        self.max_mana = 0
        self.mana = 0
        self.used_card_in_turn = []

        self.opponent_hero = 0
        self.opponent_health = 30
        self.opponent_mana = 0
        self.opponent_hand_num = 0
        self.used_card_in_opponent_turn = []

        self.turn = 0

        # 手札
        self.player_hand = []

        # 盤面
        self.player_board = []
        self.opponent_board = []
    
    def set_player(self):
        pass

    def player_update(self):
        pass

    def hand_update(self):
        pass

    def board_update(self):
        pass

    def output_game_state(self):
        pass