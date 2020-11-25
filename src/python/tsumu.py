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

# 中心周辺の色を平均可してツムを色にする
def averageColor(crop, ancestor):
    # RGB平均値を出力
    # flattenで一次元化しmeanで平均を取得 
    b = crop.T[0].flatten().mean()
    g = crop.T[1].flatten().mean()
    r = crop.T[2].flatten().mean()

    if b == "nan" or g == "nan" or r == "nan":
        b = 255
        g = 255
        r = 255
    
    # ダサすぎる
    if b <= 85:
        b = 40
    elif 85 < b <= 170:
        b = 120
    elif 170 < b <=255:
        b = 210
    
    if g <= 85:
        g = 40
    elif 85 < g <= 170:
        g = 120
    elif 170 < g <=255:
        g = 210

    if r <= 85:
        r = 40
    elif 85 < r <= 170:
        r = 120
    elif 170 < r <=255:
        r = 210

    if r == 210 or g == 210 or b == 210:
        if r < 210:
            r = 0
        if g < 210:
            g = 0
        if b < 210:
            b = 0

    color = {
        "blue": b,
        "green": g,
        "red":r
    }
    return color

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

# ルートを検索する処理
# param 円の情報の配列
def findRoute(group):
    # 開始ノード取得
    start = getStartNode(group)
    # TODO 以下、再帰関数 つながるところからつながるところを見つける
    # TODO つながるところを発見する
    group.remove(start)
    routeArray = makeRoute(start, group, [start])
        # TODO 開始ノードが[0]で,1,2,3,4
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
    pyautogui.mouseDown(window_position[0] + 677, window_position[1] + 1450, button='left')
    pyautogui.mouseUp(window_position[0] + 677, window_position[1] + 1450, button='left')

def connectTsumu(array):
    # ここからPCのカーソルを操作する
    # 中心点を繋ぐ処理
    first = True
    index = 0
    for i in array:
        # 移動
        pyautogui.moveTo(window_position[0] + int(i["center_x"]), 450 + window_position[1] + int(i["center_y"]), duration=0.01)
        if first:
            # スタート地点からクリックする
            pyautogui.mouseDown(window_position[0] + int(i["center_x"]), 450 + window_position[1] + int(i["center_y"]), button='left')
            first = False
        index += 1
        if index == len(array):
            # クリックを解除
            pyautogui.mouseUp(window_position[0] + int(i["center_x"]), 450 + window_position[1] + int(i["center_y"]), button='left')


def main():
    try:
        while True:
            # 処理の最初でスクショを取得する
            logging.info('info %s', 'sukusyo')
            capture()
            logging.info('info %s', 'sukusyo owari')
            # 取得したスクショをいじる
            img = cv2.imread(img_path,0)
            color_img = cv2.imread(img_path)
            ancestor = cv2.imread(img_path)

            # コントラスト、明るさを変更する。
            constract = gamma_correction(ancestor, gamma=2.5)
            
            # トリミング
            x, y = 0, 450
            h, w = 950, 920
            ancestor = constract[y:y+h, x:x+w]
            color_img = color_img[y:y+h, x:x+w]
            img = img[y:y+h, x:x+w]

            
            circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,80,param1=50,param2=20,minRadius=35,maxRadius=60)
            circles = np.uint16(np.around(circles))

            cercle_info = []
            for i in circles[0,:]:
                # 中心周辺の色を取得する
                crop = ancestor[i[1]-10:i[1]+10, i[0]-10:i[0]+10]
                color = averageColor(crop, ancestor)

                cercle_info.append({
                    "color": color,
                    "center_x": i[0],
                    "center_y": i[1],
                })

            all_list = []
            for k in cercle_info:
                cv2.circle(
                    color_img,
                    (k["center_x"], k["center_y"]),
                    50,
                    (k["color"]["blue"], k["color"]["green"], k["color"]["red"]),
                    -1
                )
                # 色の種類
                all_list.append(
                    {
                    "blue": k["color"]["blue"],
                    "green": k["color"]["green"],
                    "red": k["color"]["red"]
                    }
                )

            color_list = getUniqueList(all_list)

            # 色ごとにグループ化
            group = []
            for i in color_list:
                sub = []
                for j in cercle_info:
                    if i["blue"] == j["color"]["blue"] and i["green"] == j["color"]["green"] and i["red"] == j["color"]["red"]:
                        sub.append(j)
                
                if len(sub) >= 3:
                    group.append(sub)
            color_group = []
            for i in group:
                color_group.append(findNearPlaceTsumu(i))

            # 繋げるツムの選択
            most_length = 0
            use_group = None
            for i in color_group:
                for k in i:
                    if len(k) > most_length:
                        most_length = len(k)
                        use_group = k
            # ルート検索,なぞる順に配列を作る
            array = findRoute(getUniqueList(use_group))
            if len(array) < 3:
                tapFan()
                continue
            connectTsumu(array)
    except KeyboardInterrupt:
        print('!!FINISH!!')

    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()