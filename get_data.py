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
    get_replay(wait,log)

    pass

def get_replay(wait,log):
    # ゲームの再生
    g = game.Game()

    # todo: 行動履歴を基にゲームを再生して、状態を取る
    # todo: 相手のカードは伏せる
    # todo: プレイヤー名をどっかからか取得する playerとopponent
    # todo: カードのデータは他のxmlファイルから取得してくる
    # todo: 



    for l in log:
        print("action: {}".format(l.get_attribute("textContent")))

    
    pass

if __name__ == "__main__":
    #実行
    subprocess.Popen.__init__ = _patched_constructor
    #count_deck_type(mode=True,num=10000)
    move(mode=True,num=1)