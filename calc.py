import os
import cv2
import numpy as np
from itertools import combinations, permutations

# testSrc = [[136,465],[304,236],[391,459],[493,411]]
# testDst = [[230,292],[316,171],[364,288],[418,260]]
testSrc = '136,465,304,236,391,459,493,411,178,342,211,76,78,83,83,189'
testDst = '230,292,316,171,364,288,418,260,250,227,268,84,193,90,198,145'


def onMouse1(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("src:", x, y)


def onMouse2(event, x, y, flag, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("dst:", x, y)


def point():
    img1 = cv2.imread('/home/mayui/code/minio_server/img/939810332082177/1.jpg')
    img2 = cv2.imread('/home/mayui/code/minio_server/img/939810332082176/1.jpg')
    cv2.namedWindow("img1", 1)
    cv2.namedWindow("img2", 1)
    cv2.setMouseCallback("img1", onMouse1)
    cv2.setMouseCallback("img2", onMouse2)
    cv2.imshow("img1", img1)
    cv2.imshow("img2", img2)
    cv2.waitKey(0)


def kk(a, b):
    aaa = False
    bbb = False
    for aa in list(permutations(a, 3)):
        aaa = aaa or kkk(aa[0][0], aa[0][1], aa[1][0], aa[1][1], aa[2][0], aa[2][1])
    for bb in list(permutations(b, 3)):
        bbb = bbb or kkk(bb[0][0], bb[0][1], bb[1][0], bb[1][1], bb[2][0], bb[2][1])
    return aaa and bbb


def kkk(x1, y1, x2, y2, x3, y3):
    k = ((x1 - x3) * (y2 - y3) - (x2 - x3) * (y1 - y3)) / 2
    if k == 0:
        return True
    else:
        return False


def calc(src, dst, visible_mottxt_path, infrared_mottxt_path, width, height):
    a = [int(x) for x in src.split(',')]
    b = [int(x) for x in dst.split(',')]
    srcPoints = np.float32(a)
    dstPoints = np.float32(b)
    srcPoints.resize((len(srcPoints) // 2, 2))
    dstPoints.resize((len(dstPoints) // 2, 2))
    # print(srcPoints,dstPoints)
    if kk(srcPoints, dstPoints):
        print("三点共线，无法缩放")
    else:
        H, _ = cv2.findHomography(srcPoints=srcPoints, dstPoints=dstPoints, method=cv2.RANSAC,
                                  ransacReprojThreshold=5.0)
        # srcPoints.resize([4, 1, 2])
        # srcPoints_ = np.array([[[21, 21],
        #                [21, 24],
        #                [24, 21],
        #                [24, 24]]], dtype=srcPoints.dtype)
        # MM = cv2.perspectiveTransform(src=srcPoints_, m=H)
        with open(visible_mottxt_path, encoding='utf-8') as f:
            lines = f.readlines()

        if not os.path.exists(infrared_mottxt_path[:-7]):
            os.mkdir(infrared_mottxt_path[:-7])
        f_mot_txt = open(infrared_mottxt_path, 'w')

        for line in lines:
            line_list = line.split()
            isin, cor_new = get_cor(line_list[2:], H, int(width), int(height))
            if isin:
                str_list = []
                str_list.extend(line_list[:2])
                str_list.extend([int(x) for x in cor_new])
                f_mot_txt.write(" ".join(str(x) for x in str_list) + '\n')

        f_mot_txt.close()

        # print(H)
        # print(MM)
    # with open(save_txt, 'w') as f:
    #     f.write(str(H))


def get_cor(old_cor, H, width, height):
    old_cor = [int(x) for x in old_cor]
    old_cor = np.float32(old_cor)
    old_cor.resize((2, 1, 2))
    new_cor = cv2.perspectiveTransform(src=old_cor, m=H)
    new_cor.resize(4)
    cor_new = []
    if not (new_cor[2] >= 0 and new_cor[3] >= 0):
        return False, [0, 0, 0, 0]
    elif not (new_cor[0] <= width and new_cor[1] <= height):
        return False, [0, 0, 0, 0]
    else:
        cor_new.append(new_cor[0] if new_cor[0] >= 0 else 0)
        cor_new.append(new_cor[1] if new_cor[1] >= 0 else 0)
        cor_new.append(new_cor[2] if new_cor[2] <= width else width)
        cor_new.append(new_cor[3] if new_cor[3] <= height else height)
        return True, cor_new


if __name__ == '__main__':
    import sys

    # x_old = "10,10,15,10,10,15,15,15"
    # x_new = "0,0,5,0,0,5,5,5"
    # calc(x_old, x_new, "./mot.txt", "../mot.txt", 360, 360)
    calc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
# point()
