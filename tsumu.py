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
    color = {
        "blue": b,
        "green": g,
        "red":r
    }
    return color

def main():
    # TODO 処理の最初でスクショを取得する
    # 取得したスクショをいじる
    img = cv2.imread('./img/tumu1.jpg',0)
    color_img = cv2.imread('./img/tumu1.jpg')
    ancestor = cv2.imread('./img/tumu1.jpg')
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

    for k in center_list:
        cv2.circle(
            color_img,
            (k["center_x"], k["center_y"]),
            100,
            (k["color"]["blue"], k["color"]["green"], k["color"]["red"]),
            -1
        )


    # TODO 同じ色で、円が3つ以上重なっている箇所を検知する
    # TODO 検知した3つ以上の円の中心点を取得する。
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