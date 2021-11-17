import os
from typing import ValuesView
from hsreplay.elements import GameEntityNode, TagNode
import requests
import datetime
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import subprocess
from hsreplay.document import HSReplayDocument as hsd
import hsreplay.utils as hsu
import hslog

# xmlファイルを解読する

# 見やすくして保存
def annotate():
    path = os.getcwd()
    xml_file = path + "/replay/test.xml"
    read_file = path + "/read/test.xml"

    # アノテーション
    game = hsd.from_xml_file(xml_file)
    hsu.annotate_replay(xml_file, read_file)

# 必要なデータの取り出し
def get_step():
    # 1step毎のデータを取り出す
    pass


if __name__ == "__main__":
    annotate()