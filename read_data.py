import os
import requests
import datetime
import urllib.request as req
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import subprocess
from hsreplay.document import HSReplayDocument
import hslog


def read():
    path = os.getcwd()
    path = path + "/replay/test.xml"

    game = HSReplayDocument.from_xml_file(path)
    print(game)

if __name__ == "__main__":
    read()