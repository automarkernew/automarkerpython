# -*- coding: UTF-8 -*-
"""
@Project ：kalman-filter-in-single-object-tracking 
@File ：measure.py
@Date ：9/15/21 11:30 AM 
"""
import os
import numpy as np
import cv2
import const


def load_measurement(file_dir):
    """
    根据file目录，产生观测list
    :param file_dir: 每帧观测分别对应一个txt文件，每个文件中多个目标观测逐行写入
    :return: 所有观测list，[[帧1所有观测],[帧2所有观测]]
    """
    mea_list = []
    file_path = os.path.join(file_dir, "detect.txt")
    cnt = 1
    mea1 = [0]
    mea_frame_list = []
    with open(file_path, "r") as f:
        for _, mea in enumerate(f.readlines()):
            mea = mea.replace('\n', "").split(" ")
            if mea[0] != mea1[0] and cnt > 1:
                mea_list.append(mea_frame_list)
                mea_frame_list = []
            mea_frame_list.append(np.array(mea[1:5], dtype="float"))  # tl_x, tl_y, br_x, br_y
            mea1 = mea
            cnt += 1
        mea_list.append(mea_frame_list)
    return mea_list



if __name__ == "__main__":
    mea_list = load_measurement('C:/Users/Lenovo/Desktop/txt/')
    print(mea_list[9])

    # for mea_frame_list in mea_list:
    #     ret, frame = cap.read()
    #     for mea in mea_frame_list:
    #         # print(mea)
    #         cv2.rectangle(frame, tuple(mea[:2]), tuple(mea[2:]), const.COLOR_MEA, thickness=1)
    #
    #     cv2.imshow('Demo', frame)
    #     cv2.waitKey(100)  # 显示 1000 ms 即 1s 后消失
    #
    # cap.release()
    # cv2.destroyAllWindows()
