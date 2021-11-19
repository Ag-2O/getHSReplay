import os
from hsreplay.document import HSReplayDocument as hsd
import hsreplay.utils as hsu
import xml.etree.ElementTree as ET

# xmlファイルを解読する

# 見やすくして保存
def annotate():
    path = os.getcwd()
    xml_file = path + "/replay/log_20211117_023415.xml"
    read_file = path + "/read/out_20211117_023415.xml"

    # アノテーション
    game = hsd.from_xml_file(xml_file)
    hsu.annotate_replay(xml_file, read_file)

# 必要なデータの取り出し
def get_step():
    # 1step毎のデータを取り出す
    path = os.getcwd()
    xml = path + "/read/out_20211117_023415.xml"

    # xmlファイルの解析
    tree = ET.parse(xml)
    root = tree.getroot()

    print("tag: {}".format(root.tag))
    print("attrib: {}".format(root.attrib))

    child = root[0]
    print("tag: {}".format(child.tag))
    print("attrib: {}".format(child.attrib))

    for ch in child.findall("Block"):
        #print("Block : {}".format(ch.attrib))
        for c in ch.findall("TagChange"):
            health = ""
            attack = ""
            if c.attrib["tag"] == "45":
                health = c.attrib["value"]
            if c.attrib["tag"] == "47":
                attack = c.attrib["value"]
            print("health : {}, attack : {}".format(health,attack))
            #print("    TagChange : {}, health : {}, attack : {}".format(c.attrib,health,attack))
        print("\n")

    pass

if __name__ == "__main__":
    #annotate()
    get_step()