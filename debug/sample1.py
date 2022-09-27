import cv2
import numpy as np
import math
import pyautogui
import sys

img_path = "../img/sample.png"
# windowの左上角の座標を取得する
window_position = pyautogui.position()

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
                    if 0 < math.sqrt(x+y) <= 140:
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
                        if 0 < math.sqrt(x+y) <= 140:
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
            if 0 < math.sqrt(x+y) <= 140:
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
        if 0 < math.sqrt(x+y) <= 140:
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
    pyautogui.mouseDown(window_position[0] + 612, window_position[1] + 1316, button='left')
    pyautogui.mouseUp(window_position[0] + 612, window_position[1] + 1316, button='left')

def connectTsumu(array):
    # ここからPCのカーソルを操作する
    # 中心点を繋ぐ処理
    first = True
    index = 0
    for i in array:
        # 移動
        pyautogui.moveTo(window_position[0] + int(i["center_x"]), window_position[1] + int(i["center_y"]), duration=0.1)
        if first:
            # スタート地点からクリックする
            pyautogui.mouseDown(window_position[0] + int(i["center_x"]),window_position[1] + int(i["center_y"]), button='left')
            first = False
        index += 1
        if index == len(array):
            # クリックを解除
            pyautogui.mouseUp(window_position[0] + int(i["center_x"]),window_position[1] + int(i["center_y"]), button='left')

def gamma_correction(img, gamma):
    # テーブルを作成する。
    table = (np.arange(256) / 255) ** gamma * 255
    # [0, 255] でクリップし、uint8 型にする。
    table = np.clip(table, 0, 255).astype(np.uint8)

    return cv2.LUT(img, table)

def hsv_decision(rgb):
    # k means を使用する
    Z = rgb.reshape((-1,3))
    # convert to np.float32
    Z = np.float32(Z)
    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    K = 4
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((rgb.shape))
    cv2.imshow('res2',res2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # TODO k-meansした中で一番割合の大きい色のRGBを抽出(k=1で解決？)
    # TODO hsv -> RGBに変更
    return {
        "h": 1,
        "s": 2,
        "v": 3
    }

def main():
    # 処理の最初でスクショを取得する
    # capture()
    # 取得したスクショをいじる
    img = cv2.imread(img_path,0)
    color_img = cv2.imread(img_path)
    ancestor = cv2.imread(img_path)

    # トリミング
    # x, y = 0, 450
    # h, w = 800, 720
    # color_img = color_img[y:y+h, x:x+w]
    # img = img[y:y+h, x:x+w]

    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,50,param1=60,param2=15,minRadius=35,maxRadius=45)
    circles = np.uint16(np.around(circles))

    cercle_info = []
    for i in circles[0,:]:
        # 中心周辺の色を取得する
        crop = ancestor[i[1]-45:i[1]+45, i[0]-45:i[0]+45]

        hsv_color = hsv_decision(crop)

        cercle_info.append({
            "color": hsv_color,
            "center_x": i[0],
            "center_y": i[1],
        })

    all_list = []
    for k in cercle_info:
        cv2.circle(
            color_img,
            (k["center_x"], k["center_y"]),
            45,
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
            print("create group")
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
    
    if use_group != None:
        # ルート検索,なぞる順に配列を作る
        array = findRoute(getUniqueList(use_group))
        print(array)
    else:
        print("tapFan")
        tapFan()
            
    if len(array) < 3:
        tapFan()
        print("tapFan3IKA")

    ############# Debug
    cv2.imshow('color', color_img)
    # cv2.imshow('sss', ancestor)
    cv2.imshow('vanila',ancestor)
    ############# Debug END

    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()