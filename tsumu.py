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

def main():
    # TODO 処理の最初でスクショを取得する
    # 取得したスクショをいじる
    img = cv2.imread('./img/tumu.jpg',0)
    color_img = cv2.imread('./img/tumu.jpg')
    ancestor = cv2.imread('./img/tumu.jpg')
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
        cv2.circle(color_img,(i[0],i[1]),i[2],(0,255,0),8)
        # draw the center of the circle
        cv2.circle(color_img,(i[0],i[1]),2,(0,0,255),7)
        # push crop image
        crop = ancestor[i[1]-90:i[1]+90, i[0]-90:i[0]+90]
        print(crop)
        center_list.append(crop)

    for i in center_list:
        # RGB平均値を出力
        # flattenで一次元化しmeanで平均を取得 
        b = i.T[0].flatten().mean()
        g = i.T[1].flatten().mean()
        r = i.T[2].flatten().mean()

        if b == "nan" or g == "nan" or r == "nan":
            b = 255
            g = 255
            r = 255
        pts = np.array( [ [0,0], [0,180], [180, 180], [180,0] ] )
        dst = cv2.fillPoly(ancestor, pts =[pts], color=(b,g,r))
        center_list = cv2.fillPoly(i, pts =[pts], color=(b,g,r))

    # TODO 同じ色で、円が3つ以上重なっている箇所を検知する
    # TODO 検知した3つ以上の円の中心点を取得する。
    # ここからPCのカーソルを操作する
    # TODO 中心点を繋ぐ処理　

    dst_resize = resize(dst)
    cv2.namedWindow('result', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('result', dst_resize[0], dst_resize[1])
    cv2.imshow('result', dst)
    size = resize(color_img)
    cv2.namedWindow('color', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('color', size[0], size[1])
    cv2.imshow('color',color_img)


    # end process
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()