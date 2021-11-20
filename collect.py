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
        driver.get(link)
        sleep(1)

        # リプレイの解読
        get_replay(driver)

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

def get_replay(driver):

    # todo: 状態遷移毎に取得するようにしたい
    # todo: 遷移のあるサイトのスクレイピングを調べる
    # todo: win/loseを取得出来たら繰り返しを止める
    # todo: 1step毎に取るようにしたい
    # todo: カードの効果中に状態を取得したくない -> なんか文字列取得できてたらpassするとか？try/exceptで
    # todo: 手札と盤面の情報も取りたい
    # todo: 全体でタイミングを合わせる必要がある -> 作り直しするべきでは？
    # todo: 可能であればxmlの方が良い

    n = 0
    while(n < 50):
        sleep(2)
        # プレイヤー情報
        get_player_info(driver)

        # 手札情報
        get_hand_info(driver)

        # 盤面情報
        get_board_info(driver)

        # ターン毎に使ったカードの取得
        get_play_history(driver)

        # 1ステップ進める
        step(driver)

        # ゲーム終了 → ループから抜ける
        if finish():
            break

        n += 1

def get_player_info(driver):
    # プレイヤー情報の取得
    # プレイヤーの体力
    # プレイヤーの最大マナ
    # プレイヤーのマナ
    # 相手の体力
    # 相手のマナ

    try:
        # プレイヤーのターン
        player_info = driver.find_element_by_class_name("player.current")
        opponent_info = driver.find_element_by_class_name("player.top")
    except:
        # 相手のターン
        #player_info = driver.find_element_by_class_name("player")
        #opponent_info = driver.find_element_by_class_name("player.top.current")
        return

    try:
        health = player_info.find_element_by_class_name("entity.in-play.hero").find_element_by_class_name("stats").find_element_by_class_name("health").get_attribute("textContent")
    except:
        health = player_info.find_element_by_class_name("entity.in-play.hero").find_element_by_class_name("stats").find_element_by_class_name("health.negative").get_attribute("textContent")


    player_mana = player_info.find_element_by_class_name("details").find_element_by_class_name("tray").find_element_by_tag_name("span")
    player_max_mana = player_mana.get_attribute("textContent")[2]
    player_current_mana = player_mana.get_attribute("textContent")[0]
    
    try:
        op_health = opponent_info.find_element_by_class_name("entity.in-play.hero").find_element_by_class_name("stats").find_element_by_class_name("health").get_attribute("textContent")
    except:
        op_health = opponent_info.find_element_by_class_name("entity.in-play.hero").find_element_by_class_name("stats").find_element_by_class_name("health.negative").get_attribute("textContent")
    
    op_mana = opponent_info.find_element_by_class_name("details").find_element_by_class_name("tray").find_element_by_tag_name("span")
    op_max_mana = op_mana.get_attribute("textContent")[2]

    op_hand_num = len(opponent_info.find_element_by_class_name("entity-list.hand").find_elements_by_tag_name("li"))

    print("health: {}, max_mana: {}, current_mana: {}".format(health,player_max_mana,player_current_mana))
    print("op_health: {}, op_mana: {}, op_hand_num: {}".format(op_health,op_max_mana,op_hand_num))
    print("----------------------------------------------------------------------------")

def get_hand_info(driver):
    # 手札情報の取得
    # カードの種類
    # カードのコスト
    # 体力
    # 攻撃力
    # 効果の有無
    pass

def get_board_info(driver):
    # 盤面情報の取得
    # 自分のカードの情報
    # 相手のカードの情報
    pass

def get_play_history(driver):
    # ターン毎に使ったカードの取得
    pass

def step(driver):
    # ステップ進行
    
    pass

def finish():
    # ゲーム終了かどうか
    pass


def count_deck_type(mode=True,num=10):
    # driverの設定
    options = Options()
    if mode:
        options.add_argument("--headless")
    options.add_argument('--log-level=1')
    driver_path = os.getcwd()
    driver = webdriver.Chrome(driver_path+"/chromedriver", options=options)
    wait = WebDriverWait(driver, 3)

    dt = DeckType()

    # HSreplayを開く
    driver.get('https://hsreplay.net/?hl=ja')
    sleep(1)

    for n in range(num):
        print("Iter: {}".format(n))

        try:
            live_data = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'replay-feed-item')))
            deck = live_data.find_elements_by_tag_name("span")
            deck_name1 = deck[0].get_attribute("textContent")

            # デッキのカウント
            dt.deck_count(deck_name1)
        except:
            continue
    
    dt.print_deck_type()
    print("complete!")

    driver.close()
    driver.quit()

# urlからダウンロード
def download_files(url):
    # ダウンロード
    response = requests.get(url)
    
    # ファイル名
    path = os.getcwd()
    now = datetime.datetime.now()
    filename = "log_"+now.strftime('%Y%m%d_%H%M%S')+".xml"
    
    # Responseのチェック
    try:
        response_status = response.raise_for_status()
    except Exception as exc:
        print("Error:{}".format(exc))
    
    # Responseが正常なら
    if response_status == None:

        # ファイル生成
        with open(path+"/warriarVSdruid/"+filename,"w") as file:
            file.write(response.text)

        print("done!")

class DeckType:
    def __init__(self):
        # デッキの種類のカウント
        self.deck_dict = {}

    def deck_count(self,deck_name):
        # カウント
        if deck_name in self.deck_dict.keys():
            self.deck_dict[deck_name] += 1
        else:
            self.deck_dict[deck_name] = 1
    
    def print_deck_type(self):
        # 出力
        sum_value = 0
        sort_dict = sorted(self.deck_dict.items(), key=lambda x:x[1], reverse=True)
        for item in sort_dict:
            print("deck_type: {}, num: {}".format(item[0],item[1]))
            sum_value += item[1]
        print("deck_type_sum: {}".format(sum_value))

if __name__ == "__main__":
    #実行
    subprocess.Popen.__init__ = _patched_constructor
    #count_deck_type(mode=True,num=10000)
    move(mode=True,num=1)