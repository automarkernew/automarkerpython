import cv2
import numpy as np
import os
import random


def load_measurement(file_dir):
    """
    根据file目录，产生观测list
    :param file_dir: 每帧观测分别对应一个txt文件，每个文件中多个目标观测逐行写入
    :return: 所有观测list，[[帧1所有观测],[帧2所有观测]]
    """
    mea_list = []
    file_path = os.path.join(file_dir) #, "mot.txt")
    cnt = 1
    mea1 = [0]
    mea_frame_list = []
    with open(file_path, "r") as f:
        for _, mea in enumerate(f.readlines()):
            mea = mea.replace('\n', "").split(" ")
            if mea[0] != mea1[0] and cnt > 1:
                mea_list.append(mea_frame_list)
                mea_frame_list = []
            mea_frame_list.append(np.array(mea[0:6], dtype="float"))  # tl_x, tl_y, br_x, br_y
            mea1 = mea
            cnt += 1
        mea_list.append(mea_frame_list)
    return mea_list


def del_file(path_data):
    for i in os.listdir(path_data):
        path_file = os.path.join(path_data, i)
        if os.path.isfile(path_file):
            os.remove(path_file)
        else:
            for f in os.listdir(path_file):
                path_file2 = os.path.join(path_file, f)
                if os.path.isfile(path_file2):
                    os.remove(path_file2)
    for i in os.listdir(path_data):  # os.listdir(path_data)#返回一个列表，里面是当前目录下面的所有东西的相对路径
        file_data = os.path.join(path_data, i)  # 当前文件夹的下面的所有东西的绝对路径
        os.rmdir(file_data)


def paint(path2, path1, path3):
    if not os.path.exists(str(path3)):
        os.mkdir(str(path3))
    del_file(path3)
    # 载入mot算法产生的轨迹坐标值
    meas_list_all = load_measurement(str(path1))
    a = 1  # 第一个目标编号
    mea = []
    colour = []
    cap = cv2.VideoCapture(str(path2))  # 穿插着视频是为了方便展示
    cnt = 1
    # 给每个物体赋予颜色
    for i in range(int(meas_list_all[-1][0][1])):
        colour.append([random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)])

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        for meas_list_frame in meas_list_all:
            if meas_list_frame[0][1] == a and meas_list_frame[0][0] <= cnt \
                    and cnt > 1:
                mea.append(meas_list_frame[0])
            # print('a' + str(mea))
            if ((meas_list_frame[0][1] != a and cnt > 1) or (
                    all(meas_list_frame[0] == meas_list_all[0][-1]) and cnt > 1)) \
                    and mea:
                if mea[0][0] >= (cnt - 8):  # 轨迹消失后最多保留8帧
                    # print('b' + str(mea[0]))
                    for i in range(len(mea) - 1):
                        x1 = int((mea[i][2] + mea[i + 1][4]) / 2)
                        y1 = int((mea[i][3] + mea[i + 1][5]) / 2)
                        x2 = int((mea[i + 1][2] + mea[i + 1][4]) / 2)
                        y2 = int((mea[i + 1][3] + mea[i + 1][5]) / 2)
                        cv2.line(frame, (x1, y1), (x2, y2), colour[int(mea[i][1]) - 1], 2)
                mea = []
            a = meas_list_frame[0][1]
        # cv2.namedWindow('Demo', 0)
        # cv2.imshow('Demo', frame)
        cv2.imwrite(str(path3) + str(cnt) + '.jpg', frame)
        # k = cv2.waitKey(0)  # 显示 1000 ms 即 1s 后消失
        # if k == 27:
        #     break
        cnt += 1


if __name__ == '__main__':
    # paint('/home/hdtx/code/minio_servervideo/898560719585359/5zhen.mp4',
    #       'D:/303Project/gsb_business-master/data/mottxt/805808560406528/mot.txt',
    #       'D:/303Project/gsb_business-master/data/motimg/805808560406528/')
    import sys

    paint(sys.argv[1], sys.argv[2], sys.argv[3])
