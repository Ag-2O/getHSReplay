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


# xmlファイルから必要な情報のみでゲームを再生


class Card:
    def __init__(self):
        self.cost = 0
        self.effect = 0

class Minion(Card):
    def __init__(self, cost, health, attack, effect, can_attack):
        self.card_type = 1
        self.cost = cost
        self.health = health
        self.attack = attack
        self.effect = effect
        self.can_attack = can_attack
    
    def show_stats(self):
        return {"cost":self.cost,
                "health":self.health,
                "attack":self.attack,
                "effect":self.effect,
                "cam_attack":self.can_attack}

class Spell(Card):
    def __init__(self, cost):
        self.card_type = 2
        self.cost = cost

    def show_stats(self):
        return {"cost":self.cost}

class Weapon(Card):
    def __init__(self, durable, attack, effect):
        self.card_type = 3
        self.attack = attack
        self.durable = durable
        self.effect = effect

class Seclet(Card):
    def __init__(self, effect):
        self.card_type = 4
        self.effect = effect

# ゲーム情報

class GameState:
    def __init__(self,tree):
        # ゲーム
        self.game = tree[0]

        # プレイヤー情報
        self.player_health = 30
        self.max_mana = 0
        self.current_mana = 0
        self.player_hero = 0

        self.opponent_health = 30
        self.opponent_mana = 0
        self.opponent_hand_num = 0
        self.opponent_hero = 0

        self.turn = 0

        # 手札
        self.hand = []

        # 盤面
        self.board = []

    
    def progress_game(self):
        # ブロックの取得
        bl = self.game.findall("Block")

        # 初期手札の取得
        self.init_hand(bl[0])

        # マリガン
        self.mulligan()

        # ゲームスタート
    
    def init_hand(self,block):
        # 初期手札
        show_entity = block.findall("ShowEntity")
        for se in show_entity:
            card_id = se.attrib["cardID"]
            tag = se.findall("Tag")
            card_type = 0
            for t in tag:
                if "GameTagName" in t.attrib.keys():
                    if "CARDTYPE" == t.attrib["GameTagName"]:
                        if "4" == t.attrib["value"]:
                            # ミニオン
                            card_type = 1
                        elif "5" == t.attrib["value"]:
                            # スペル
                            card_type = 2
                        elif "6" == t.attrib["value"]:
                            # ウェポン
                            card_type = 3
                        else:
                            # シークレット
                            card_type = 4
                    
                    if "COST" == t.attrib["GameTagName"]:
                        card_cost = t.attrib["value"]
                        
                    if card_type == 1:
                        # 体力と攻撃力の取得
                        if "HEALTH" == t.attrib["GameTagName"]:
                            card_health = t.attrib["value"]
                        elif "ATK" == t.attrib["GameTagName"]:
                            card_attack = t.attrib["value"]
            
            if card_type == 1:
                self.hand.append(Minion(card_cost, card_health, card_attack, 1, 0))
            elif card_type == 2:
                self.hand.append(Spell(card_cost))
            elif card_type == 3:
                pass
                #Weapon(card_cost)
            else:
                pass
                #Secret(card_cost)
        
        # 後攻の場合、コインの追加
        full_entity = block.findall("FullEntity")
        for fe in full_entity:
            card_id = fe.attrib["cardID"]
            if card_id == "SW_COIN2":
                card_cost = 0
                self.hand.append(Spell(card_cost))
            else:
                print("unknown card in hand")
        
        # test
        for h in self.hand:
            print("hand: {}".format(h.show_stats()))
    
    def mulligun(self):
        # マリガン処理
        pass


    def get_deck(self):
        # 使ったカードの読み込み
        with open("card_id.json","rb") as ci:
            self.card_id = json.load(ci)

        # デッキの取得
        me = self.game.findall("Player")[1]
        for c in me.find("Deck").findall("Card"):
            # カードに番号を振る
            card_id = c.attrib["id"]
            if card_id not in self.card_id.keys():
                self.card_id[card_id] = len(self.card_id)
        
        # jsonに保存
        with open("card_id.json","w") as ci:
            json.dump(self.card_id,ci)


if __name__ == "__main__":
    # test
    path = os.getcwd()
    xml = path + "/read/out_20211117_023415.xml"
    tree = ET.parse(xml)
    root = tree.getroot()
    gs = GameState(tree=root)
    gs.progress_game()
