import pandas as pd
import xml.etree.ElementTree as ET
from xml.dom import minidom

def create_net_file(output_path="sumo/generated.net.xml"):
    """
    単純な直線道路を持つSUMOネットワークファイルを作成する。
    """
    # ノードとエッジの定義
    nodes = [
        {'id': '1', 'x': '0.0', 'y': '0.0'},
        {'id': '2', 'x': '2000.0', 'y': '0.0'}
    ]
    edges = [
        {'id': '1_to_2', 'from': '1', 'to': '2', 'priority': '1', 'numLanes': '3', 'speed': '13.89'}
    ]

    # XML構造の作成
    net = ET.Element('net')
    net.set('version', '1.1')

    for node_data in nodes:
        node = ET.SubElement(net, 'node')
        for key, val in node_data.items():
            node.set(key, val)

    for edge_data in edges:
        edge = ET.SubElement(net, 'edge')
        for key, val in edge_data.items():
            edge.set(key, val)

    # XMLを整形して保存
    xml_str = ET.tostring(net, 'utf-8')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open(output_path, "w") as f:
        f.write(pretty_xml_str)
    print(f"ネットワークファイルを作成しました: {output_path}")

def create_rou_file(csv_path, output_path="sumo/generated.rou.xml"):
    """
    追跡結果CSVからSUMOルートファイルを作成する。
    """
    df = pd.read_csv(csv_path)

    # XML構造の作成
    routes = ET.Element('routes')

    # オブジェクトの種類ごとにvTypeを定義
    # class_nameとSUMOのvClassのマッピング
    vclass_map = {
        'person': 'pedestrian',
        'bicycle': 'bicycle',
        'car': 'passenger',
        'motorcycle': 'motorcycle',
        'bus': 'bus',
        'truck': 'truck'
    }

    # 追跡IDごとに処理
    for track_id, group in df.groupby('track_id'):
        class_name = group['class_name'].iloc[0]
        vclass = vclass_map.get(class_name, 'passenger') # 不明なクラスは乗用車として扱う

        # vTypeを定義（既にあればスキップ）
        if routes.find(f"./vType[@id='{class_name}']") is None:
            vtype = ET.SubElement(routes, 'vType')
            vtype.set('id', class_name)
            vtype.set('vClass', vclass)

        # 車両（または歩行者）を定義
        vehicle = ET.SubElement(routes, 'vehicle')
        vehicle.set('id', str(track_id))
        vehicle.set('type', class_name)
        vehicle.set('depart', str(group['timestamp'].min()))

        # ルートを定義
        route = ET.SubElement(vehicle, 'route')
        route.set('edges', '1_to_2')

    # XMLを整形して保存
    xml_str = ET.tostring(routes, 'utf-8')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open(output_path, "w") as f:
        f.write(pretty_xml_str)
    print(f"ルートファイルを作成しました: {output_path}")

def create_sumocfg_file(net_file, rou_file, output_path="sumo/generated.sumocfg"):
    """
    SUMO設定ファイルを作成する。
    """
    config = ET.Element('configuration')

    input_elem = ET.SubElement(config, 'input')
    ET.SubElement(input_elem, 'net-file').set('value', net_file)
    ET.SubElement(input_elem, 'route-files').set('value', rou_file)

    time_elem = ET.SubElement(config, 'time')
    ET.SubElement(time_elem, 'begin').set('value', '0')

    # XMLを整形して保存
    xml_str = ET.tostring(config, 'utf-8')
    pretty_xml_str = minidom.parseString(xml_str).toprettyxml(indent="    ")

    with open(output_path, "w") as f:
        f.write(pretty_xml_str)
    print(f"SUMO設定ファイルを作成しました: {output_path}")

if __name__ == "__main__":
    import os

    # 出力ディレクトリ作成
    if not os.path.exists("sumo"):
        os.makedirs("sumo")

    # ファイルパス
    csv_file = "task1_simple_output/tracking_results.csv"
    net_file = "sumo/generated.net.xml"
    rou_file = "sumo/generated.rou.xml"
    sumocfg_file = "sumo/generated.sumocfg"

    # 各ファイルの生成
    create_net_file(net_file)
    create_rou_file(csv_file, rou_file)
    create_sumocfg_file(os.path.basename(net_file), os.path.basename(rou_file), sumocfg_file)

    print("SUMOファイルの生成が完了しました。")
