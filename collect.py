import requests
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
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

    # HSreplayを開く
    driver.get('https://hsreplay.net/?hl=ja')
    sleep(1)

    for n in range(num):
        # ライブデータの選択
        live_data = driver.find_elements_by_class_name("replay-feed-item")[0]
        link = live_data.get_attribute('href')
        print("replay_url {}: {}".format(n,link))
        sleep(1)

        # そのデータのサイトへ遷移
        driver.get(link)
        sleep(1)

        # xmlファイルのURL取得
        replay_xml = driver.find_element_by_class_name("infobox-settings.hidden-sm")
        xml_url = replay_xml.find_element_by_tag_name('a').get_attribute('href')
        #print("xml_url {}: {}".format(n,xml_url))
        sleep(1)

        # ダウンロード
        download_files(xml_url)

        # 元のサイトに戻る
        driver.get('https://hsreplay.net/?hl=ja')
        sleep(1)
    
    print("complete!")

    driver.close()
    driver.quit()

def trim_data():
    # 必要なデータのみにトリミング
    pass

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
        file = open(path+"/replay/"+filename,"wb")

        # 書き込み
        for chunk in response.iter_content(100000):
            file.write(chunk)

        file.close()
        print("done!")

if __name__ == "__main__":
    #実行
    subprocess.Popen.__init__ = _patched_constructor
    move(mode=True,num=10)