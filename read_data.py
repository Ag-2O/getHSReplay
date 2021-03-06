import os
from hsreplay.document import HSReplayDocument as hsd
import hsreplay.utils as hsu
import hslog
import hslog.export
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

    """
    # デッキの出力
    for pl in child.findall("Player"):
        for d in pl.findall("Deck"):
            for c in d.findall("Card"):
                print("card: {}".format(c.attrib))

    # 初期状態の出力
    for fe in child.findall("FullEntity"):
        print("card or hero: {}".format(fe.attrib))
        for t in fe.findall("Tag"):
            print("Tag : {}".format(t.attrib))
        print("\n")
    
    # 状態遷移の出力
    for tc in child.findall("TagChange"):
        print("tag_change: {}".format(tc.attrib))
    """
    # メタの出力
    for bl in child.findall("Block"):
        for md in bl.findall("MetaData"):
            if "DAMAGE" == md.attrib["MetaName"]:
                for inf in md.findall("Info"):
                    if "Nightslayer Valeera" == inf.attrib["EntityName"]:
                        print("damage: {}".format(md.attrib["data"]))
                        print("Info: {}".format(inf.attrib))


    """
    ret = hsd.from_xml(tree)
    pct = ret.to_packet_tree()
    for packet in pct:
        print("packet: {}".format(packet))
        for p in packet:
            ext = hslog.export.EntityTreeExporter(pct)
            print(ext)
    ret = ext.flush()
    print(ret)
    """

    pass



if __name__ == "__main__":
    #annotate()
    get_step()