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
import chardet
import hsreplay
import hslog


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

    # deck count
    dt = DeckType()

    # HSreplayを開く
    driver.get('https://hsreplay.net/?hl=ja')
    sleep(1)

    for n in range(num):
        print("Iter: {}".format(n))
        # ライブデータの選択
        # dekki no senntaku
        try:
            live_data = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'replay-feed-item')))
        except:
            continue
        link = live_data.get_attribute('href')
        sleep(1)

        # そのデータのサイトへ遷移
        driver.get(link)
        sleep(1)

        # xmlファイルのURL取得
        replay_xml = driver.find_element_by_class_name("infobox-settings.hidden-sm")
        xml_url = replay_xml.find_element_by_tag_name('a').get_attribute('href')
        sleep(1)

        # ダウンロード
        download_files(xml_url)

        # 元のサイトに戻る
        driver.get('https://hsreplay.net/?hl=ja')
        sleep(1)
    
    print("complete!")

    driver.close()
    driver.quit()

def count_deck_type(mode=True,num=10):
    # driverの設定
    options = Options()
    if mode:
        options.add_argument("--headless")
    options.add_argument('--log-level=1')
    driver_path = os.getcwd()
    driver = webdriver.Chrome(driver_path+"/chromedriver", options=options)
    wait = WebDriverWait(driver, 3)

    # deck count
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
            deck_name2 = deck[1].get_attribute("textContent")

            # count deck type 
            dt.deck_count(deck_name1)
            dt.deck_count(deck_name2)
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
    print(response.text)
    
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
        with open(path+"/replay/"+filename,"w") as file:
            file.write(response.text)

        print("done!")

class DeckType:
    def __init__(self):
        self.deck_dict = {}

    def deck_count(self,deck_name):
        # count deck type
        if deck_name in self.deck_dict.keys():
            self.deck_dict[deck_name] += 1
        else:
            self.deck_dict[deck_name] = 1
    
    def print_deck_type(self):
        sum_value = 0
        sort_dict = sorted(self.deck_dict.items(), key=lambda x:x[1], reverse=True)
        for item in sort_dict:
            print("deck_type: {}, num: {}".format(item[0],item[1]))
            sum_value += item[1]
        print("deck_type_sum: {}".format(sum_value))

if __name__ == "__main__":
    #実行
    subprocess.Popen.__init__ = _patched_constructor
    #move(mode=True,num=100)
    count_deck_type(mode=True,num=10000)