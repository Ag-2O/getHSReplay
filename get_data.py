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
import game

_original_constructor = subprocess.Popen.__init__


# HSReplay(https://hsreplay.net/?hl=ja)からリプレイデータを取得します


# エラー回避?????????????
def _patched_constructor(*args, **kwargs):
    for key in ('stdin', 'stdout', 'stderr'):
        if key not in kwargs:
            kwargs[key] = subprocess.PIPE

    return _original_constructor(*args, **kwargs)


# ダウンロードのページまでの移動
def move(mode=True,num=10):
    # driverの設定
    options = Options()
    if mode:
        options.add_argument("--headless")
    options.add_argument('--log-level=1')
    driver_path = os.getcwd()
    driver = webdriver.Chrome(driver_path+"/chromedriver", options=options)
    wait = WebDriverWait(driver, 3)

    # HSreplayを開く
    driver.get('https://hsreplay.net/?hl=ja')
    sleep(1)

    n = 0
    while(num > n):
        deck_name = ""
        op_deck_name = ""

        try:
            # ライブデータの選択
            live_data = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'replay-feed-item')))
            # デッキ名の取得
            deck = live_data.find_elements_by_tag_name("span")
            deck_name = deck[0].get_attribute("textContent")
            op_deck_name = deck[1].get_attribute("textContent")
        except:
            continue

        # 特定のデッキ名で無ければダウンロードしない
        #if "ウォリアー" not in deck_name or "ハンター" not in op_deck_name:
        #    continue

        print("Iter: {}, deck_name: {} vs {}".format(n,deck_name,op_deck_name))

        # リプレイのリンクを取得
        link = live_data.get_attribute('href')
        sleep(1)

        # そのリプレイのサイトへ遷移
        #driver.get(link)
        driver.get("https://hsreplay.net/replay/fRHRVqyNkTKv9sCCJy72pa")
        wait = WebDriverWait(driver, 3)
        sleep(1)

        # リプレイの解読
        move_replay(wait)

        # xmlファイルのURL取得
        replay_xml = driver.find_element_by_class_name("infobox-settings.hidden-sm")
        xml_url = replay_xml.find_element_by_tag_name('a').get_attribute('href')
        sleep(1)

        # ダウンロード
        #download_files(xml_url)

        # 元のサイトに戻る
        driver.get('https://hsreplay.net/?hl=ja')
        sleep(1)

        n += 1
    
    print("complete!")

    driver.close()
    driver.quit()

def move_replay(wait):
    # 行動履歴の取得
    get_history(wait)

    # プレイヤーの状態の取得
    get_player_state(wait)

    # 手札の状態の取得
    get_hand_state(wait)

    # 盤面の状態の取得
    get_board_state(wait)

    # 状態の比較
    if compare_state(wait):
        # 直前の状態と比較して同じならスルー
        pass
    else:
        # 直前の状態と比較して異なるなら保存???
        save_state()

    pass

# 行動履歴の取得
def get_history(wait):
    # 設定を開く
    scrubber = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'joust-scrubber')))
    button = scrubber.find_elements_by_tag_name("button")[3]
    button.click()
    sleep(1)

    # チェックボックスをクリック
    settings = scrubber.find_element_by_class_name("joust-scrubber-settings")
    check_box = settings.find_elements_by_xpath("//label[@class='joust-scrubber-settings-checkbox']/input")[0]
    check_box.click()
    sleep(1)

    # 行動履歴の取得
    log_bar = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'joust-log')))
    log = log_bar.find_elements_by_xpath("//div[@class='joust-log']/div")
    print("log: {}".format(log))
    for l in log:
        print("action: {}".format(l.get_attribute("textContent")))

# 両プレイヤーの状態
def get_player_state(wait):
    # プレイヤーの状態の取得
    game = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'game')))
    player_info = game.find_elements_by_xpath("//*[@id='joust-container']/div/div[1]/div[1]/div[2]/section[2]/div/section[1]/div/div[2]")
    
    for pi in player_info:
        # 攻撃力(武器持ってたり)
        atk_list = pi.find_elements_by_class_name("atk")
        if atk_list == []:
            player_atk = 0
        else:
            player_atk = atk_list[0].get_attribute("textContent")

        # 体力
        health_list = pi.find_elements_by_class_name("health")
        if health_list == []:
            health_nega_list = pi.find_elements_by_class_name("health.negative")
            if health_nega_list == []:
                player_health = health_nega_list[0].get_attribute("textContent")
        else:
            player_health = health_list[0].get_attribute("textContent")
        
        # マナ
        mana_list = pi.find_elements_by_xpath("//*[@id='joust-container']/div/div[1]/div[1]/div[2]/section[2]/div/section[2]/div[2]/span")
        player_current_mana = mana_list[0].get_attribute("textContent")[0]
        player_max_mana = mana_list[0].get_attribute("textContent")[2]
    
    print("player_info: health={} atk={} mana={}/{}".format(player_health,player_atk,player_current_mana,player_max_mana))
    
    # 敵の状態の取得
    opponent_info = game.find_elements_by_xpath("//*[@id='joust-container']/div/div[1]/div[1]/div[1]/section[1]/div/section[1]/div/div[2]")
    
    for oi in opponent_info:
        # 攻撃力(武器持ってたり)
        op_atk_list = oi.find_elements_by_class_name("atk")
        if op_atk_list == []:
            opponent_atk = 0
        else:
            opponent_atk = atk_list[0].get_attribute("textContent")

        # 体力
        op_health_list = oi.find_elements_by_class_name("health")
        if op_health_list == []:
            op_health_nega_list = oi.find_elements_by_class_name("health.negative")
            if op_health_nega_list == []:
                opponent_health = op_health_nega_list[0].get_attribute("textContent")
        else:
            opponent_health = op_health_list[0].get_attribute("textContent")
        
        # マナ
        op_mana_list = pi.find_elements_by_xpath("//*[@id='joust-container']/div/div[1]/div[1]/div[1]/section[1]/div/section[2]/div[2]/span")
        opponent_max_mana = op_mana_list[0].get_attribute("textContent")[2]
    
    print("opponent_info: health={} atk={} mana={}".format(opponent_health,opponent_atk,opponent_max_mana))
    
# 手札の取得
def get_hand_state(wait):
    # 手札の状態
    game = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'game')))
    hand_state = game.find_element_by_xpath("//*[@id='joust-container']/div/div[1]/div[1]/div[2]/section[2]/ul")
    hand_cards = hand_state.find_elements_by_tag_name("li")
    print("hand_cards: {}".format(hand_cards))

def get_board_state(wait):
    # 盤面の状態
    pass

def compare_state(wait):
    # ページ更新の比較
    # 前と変化していたら値を取得
    pass

def save_state():
    # ゲームの状態の保存
    pass

if __name__ == "__main__":
    #実行
    subprocess.Popen.__init__ = _patched_constructor
    #count_deck_type(mode=True,num=10000)
    move(mode=True,num=1)