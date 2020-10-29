import cv2
import numpy as np
import math

def resize(img):
    # resize window
    screen_res = 1280, 720
    scale_width = screen_res[0] / img.shape[1]
    scale_height = screen_res[1] / img.shape[0]
    scale = min(scale_width, scale_height)
    window_width = int(img.shape[1] * scale)
    window_height = int(img.shape[0] * scale)
    return window_width, window_height

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
    if b <= 64:
        b = 25
    elif 64 < b <= 128:
        b = 75
    elif 128 < b <=192:
        b = 125
    elif 192 < b <=255:
        b = 170
    
    if g <= 64:
        g = 25
    elif 64 < g <= 128:
        g = 75
    elif 128 < g <=192:
        g = 125
    elif 192 < g <=255:
        g = 170

    if r <= 64:
        r = 32
    elif 64 < r <= 128:
        r = 96
    elif 128 < r <=192:
        r = 160
    elif 192 < r <=255:
        r = 224

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
    before_one = []
    history = []

    # TODO all_color_groupに入っている物は比較の対象から外す様にする

    for i in group:
        first = []
        if len(near) == 0:
            before_one = i
            for j in i:
                i.remove(j)
                first = j
                color_group.append(j)
                for k in i:
                    if j == k:
                        break
                    x = (int(j["center_x"]) - int(k["center_x"])) ** 2
                    y = (int(j["center_y"]) - int(k["center_y"])) ** 2
                    if 0 < math.sqrt(x+y) <= 250:
                        near.append(k)
                        color_group.append(k)
                if len(near) != 0:
                    break
        else:
            new_near = []
            # near でforを回す
            for j in near:
                # 消した配列をまた消そうとしないためのif分
                if j not in history :
                    before_one.remove(j)
                    history.append(j)
                for k in before_one:
                    # すでに比較済みのものは何もしない
                    if k == first or k == j:
                        break

                    x = (int(j["center_x"]) - int(k["center_x"])) ** 2
                    y = (int(j["center_y"]) - int(k["center_y"])) ** 2
                    if 0 < math.sqrt(x+y) <= 250:
                        # 新たなnearができる
                        new_near.append(k)
                        color_group.append(k)
            near = new_near
            
            if len(new_near) == 0:
                all_color_group.append(color_group)
            # TODO else が終わる度にgroupのforが進んでしまうため、全てを比較することが出来ていない
    return all_color_group

def main():
    # TODO 処理の最初でスクショを取得する
    # 取得したスクショをいじる
    img_path = './img/tumu.jpg'
    img = cv2.imread(img_path,0)
    color_img = cv2.imread(img_path)
    ancestor = cv2.imread(img_path)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    a = 4
    image = cimg
    lut = [ np.uint8(255.0 / (1 + math.exp(-a * (i - 128.) / 255.))) for i in range(256)] 
    result_image = np.array( [ lut[value] for value in image.flat], dtype=np.uint8 )
    cimg = result_image.reshape(image.shape)
    
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,100,param1=65,param2=28,minRadius=67,maxRadius=130)
    circles = np.uint16(np.around(circles))
    center_list = []
    for i in circles[0,:]:
        # draw the outer circle 
        # color version
        # 円は色分けの範囲より大きめにする
        circle_size = math.floor(i[2]*1.35)
        cv2.circle(color_img,(i[0],i[1]),circle_size,(0,255,0),8)
        # draw the center of the circle
        cv2.circle(color_img,(i[0],i[1]),2,(0,0,255),7)
        # 中心周辺の色を取得する
        crop = ancestor[i[1]-30:i[1]+30, i[0]-30:i[0]+30]
        color = averageColor(crop, ancestor)

        center_list.append({
            "color": color,
            "center_x": i[0],
            "center_y": i[1],
        })

    all_list = []
    for k in center_list:
        cv2.circle(
            color_img,
            (k["center_x"], k["center_y"]),
            100,
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

    # TODO center_list rename cercle_info
    # 色ごとにグループ化
    group = []
    for i in color_list:
        sub = []
        for j in center_list:
            if i["blue"] == j["color"]["blue"] and i["green"] == j["color"]["green"] and i["red"] == j["color"]["red"]:
                sub.append(j)
        
        if len(sub) >= 3:
            group.append(sub)

    color_group = findNearPlaceTsumu(group)

    index = 0
    for i in color_group:
        print(len(i))
        for j in i:
            cv2.putText(color_img, str(index), (j["center_x"], j["center_y"]), cv2.FONT_HERSHEY_PLAIN, 4, (255, 0, 255), 5, cv2.LINE_AA)
        index += 1
        


                    # 色が三個以上だったらappend
#                    cv2.line(
#                        color_img,
#                        (j["center_x"], j["center_y"]),
#                        (k["center_x"], k["center_y"]),
#                        (255, 0, 0),
#                        5
#                    )

    # ここからPCのカーソルを操作する
    # TODO 中心点を繋ぐ処理　

    ############# Debug    
    size = resize(color_img)
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('color', size[0], size[1])
    cv2.imshow('color',color_img)
    ############# Debug END

    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()