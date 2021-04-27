import cv2
import numpy as np
import math
import pyautogui
import sys
from pywinauto import application
import logging

img_path = "./img/window.png"
args = sys.argv
# windowの左上角の座標を取得する
window_position = [int(args[2]), int(args[3])]

# ログレベルを DEBUG に変更
logging.basicConfig(filename='./dist/logger.log', level=logging.DEBUG)
# logging のみの書き方
# logging.info('info %s %s', 'test', 'test')
logging.info('info %s', args[1])
logging.info('info %s', args[2])
logging.info('info %s', args[3])


def capture():
    app = application.Application().connect(title_re="Vysor", visible_only="True")
    app[args[1]].capture_as_image().save(img_path)

def gamma_correction(img, gamma):
    # テーブルを作成する。
    table = (np.arange(256) / 255) ** gamma * 255
    # [0, 255] でクリップし、uint8 型にする。
    table = np.clip(table, 0, 255).astype(np.uint8)

    return cv2.LUT(img, table)

# ダブりを消す処理
def getUniqueList(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]

# 繋げられる距離のツムをグループ化する
# param 色ごとにグループ化したdirectry
def findNearPlaceTsumu(group):
    # 色の中でも固まっているものでグループ化
    color_group = []
    all_color_group = []
    near = []

    # TODO all_color_groupに入っている物は比較の対象から外す様にする
    gr = group

    for i in group:
        cercle_data = []
        # 比較に使用した物は削除する
        for already in color_group:
            cercle_data = already
            # 比較に使用したものから比較しようとしたらcontinue
            if already in gr:
                gr.remove(already)
        if i == cercle_data:
            continue
        
        color_group = []
        while True:
            if len(near) == 0:
                color_group.append(i)
                for k in gr:
                    x = (int(i["center_x"]) - int(k["center_x"])) ** 2
                    y = (int(i["center_y"]) - int(k["center_y"])) ** 2
                    if 0 < math.sqrt(x+y) <= 130:
                        near.append(k)
                        color_group.append(k)
                if len(near) == 0:
                    break
            else:
                new_near = []
                # near でforを回す
                for j in near:
                    for k in gr:
                        # すでに比較済みのものは何もしない
                        if k == j:
                            break
                        x = (int(j["center_x"]) - int(k["center_x"])) ** 2
                        y = (int(j["center_y"]) - int(k["center_y"])) ** 2
                        if 0 < math.sqrt(x+y) <= 130:
                            # 新たなnearができる
                            new_near.append(k)
                            color_group.append(k)
                            # color_groupをgrから消す
                            if k in gr:
                                gr.remove(k)
                near = new_near
                if len(new_near) == 0:
                    all_color_group.append(color_group)
                    break
    return all_color_group

# できる限りのルートを検索して2次元配列を返す
# group 円の情報の配列
def findRoute(group):
    # 開始ノード取得
    start = getStartNode(group)
    group.remove(start)
    routeArray = makeRoute(start, group, [start])
    return routeArray

def getStartNode(group):
    for i in group:
        node = 0
        for j in group:
            x = (int(i["center_x"]) - int(j["center_x"])) ** 2
            y = (int(i["center_y"]) - int(j["center_y"])) ** 2
            if 0 < math.sqrt(x+y) <= 130:
                node += 1
        if node == 1:
            return i
    return group[0]

def makeRoute(startNode, group, result):
    start = startNode
    nextFlag = False
    gr = group
    for i in gr:
        x = (int(start["center_x"]) - int(i["center_x"])) ** 2
        y = (int(start["center_y"]) - int(i["center_y"])) ** 2
        if 0 < math.sqrt(x+y) <= 130:
            result.append(i)
            start = i
            gr.remove(i)
            nextFlag = True
            break
            # TODO breakを消して二つあったらつながる方を選ぶようにしたい
    if not nextFlag:
        return result
    return makeRoute(start, gr, result)

def tapFan():
    pyautogui.mouseDown(window_position[0] + 550, window_position[1] + 1300, button='left')
    pyautogui.mouseUp(window_position[0] + 550, window_position[1] + 1300, button='left')
    logging.debug('debug %s', 'tapFan')

def connectTsumu(array):
    logging.debug('debug %s', 'moveMouse')
    # ここからPCのカーソルを操作する
    # 中心点を繋ぐ処理
    first = True
    index = 0
    for i in array:
        # 移動
        pyautogui.moveTo(window_position[0] + int(i["center_x"]), window_position[1] + int(i["center_y"]), duration=0.01)
        if first:
            # スタート地点からクリックする
            pyautogui.mouseDown(window_position[0] + int(i["center_x"]), window_position[1] + int(i["center_y"]), button='left')
            first = False
        index += 1
        if index == len(array):
            # クリックを解除
            pyautogui.mouseUp(window_position[0] + int(i["center_x"]), window_position[1] + int(i["center_y"]), button='left')

def hsv_decision(rgb):
    # BGRからHSVに変換
    imgBoxHsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)

    # HSV平均値を取得
    # flattenで一次元化しmeanで平均を取得 
    h = round(imgBoxHsv.T[0].flatten().mean(), 0)
    s = round(imgBoxHsv.T[1].flatten().mean(), 0)
    v = round(imgBoxHsv.T[2].flatten().mean(), 0)
        # ダサすぎる
    if h <= 36:
        h = 0
    elif 36 < h <= 72:
        h = 37
    elif 72 < h <= 108:
        h = 73
    elif 108 < h <= 144:
        h = 109
    elif 144 < h <= 180:
        h = 145
    
    if s <= 51:
        s = 0
    elif 51 < s <= 102:
        s = 52
    elif 102 < s <= 153:
        s = 103
    elif 153 < s <= 204:
        s = 154
    elif 204 < s <= 255:
        s = 205

    if v <= 51:
        v = 0
    elif 51 < v <= 102:
        v = 52
    elif 102 < v <= 153:
        v = 103
    elif 153 < v <= 204:
        v = 154
    elif 204 < v <= 255:
        v = 205

    # 小数点以下を変更

    # HSV平均値を出力
    return {
        "h": h,
        "s": s,
        "v": v
    }

def main():
    logging.info('info %s', 'mainstart')
    try:
        while True:
            # 処理の最初でスクショを取得する
            capture()
            # 取得したスクショをいじる
            img = cv2.imread(img_path,0)
            ancestor = cv2.imread(img_path)

            # コントラスト、明るさを変更する。
            constract = gamma_correction(ancestor, gamma=1.5)
            
            circles = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT,1,80,param1=50,param2=20,minRadius=35,maxRadius=60)
            circles = np.uint16(np.around(circles))

            cercle_info = []
            for i in circles[0,:]:
                # 中心周辺の色を取得する
                crop = constract[i[1]-6:i[1]+6, i[0]-6:i[0]+6]

                hsv_color = hsv_decision(crop)

                cercle_info.append({
                    "color": hsv_color,
                    "center_x": i[0],
                    "center_y": i[1],
                })

            all_list = []
            for k in cercle_info:
                cv2.circle(
                    ancestor,
                    (k["center_x"], k["center_y"]),
                    50,
                    (k["color"]["h"], k["color"]["s"], k["color"]["v"]),
                    -1
                )
                # 色の種類
                all_list.append(
                    {
                    "h": k["color"]["h"],
                    "s": k["color"]["s"],
                    "v": k["color"]["v"]
                    }
                )

            color_list = getUniqueList(all_list)

            # 色ごとにグループ化
            group = []
            for i in color_list:
                sub = []
                for j in cercle_info:
                    if i["h"] == j["color"]["h"] and i["s"] == j["color"]["s"] and i["v"] == j["color"]["v"]:
                        sub.append(j)
                
                if len(sub) >= 3:
                    group.append(sub)
                    logging.debug('debug %s', 'create Group')
            color_group = []
            for i in group:
                color_group.append(findNearPlaceTsumu(i))

            # 1つの配列にまとめる
            all_groups = sum(color_group, [])

            # 繋げるツムの選択
            use_group = []
            # 最大から3つになるまで取得
            for i in range(len(all_groups)):
                maxLength = max(len(v) for v in all_groups)
                if maxLength > 2:
                    all_groups[[len(v) for v in all_groups].index(maxLength)]
                    use_group.append(all_groups[[len(v) for v in all_groups].index(maxLength)])
                    # 大きい物から削除していく
                    all_groups.remove(all_groups[[len(v) for v in all_groups].index(maxLength)])

            # ルート検索,なぞる順に配列を作る
            # 二次元配列にして一度のループで何グループも消すようにする
            if len(use_group) == 0:
                tapFan()
                continue
            for i in use_group:
                array = findRoute(getUniqueList(i))
                if len(array) >= 3:
                    logging.debug('debu %s', len(array))
                    connectTsumu(array)
    except KeyboardInterrupt:
        print('!!FINISH!!')

    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()