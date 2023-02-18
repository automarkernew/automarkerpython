import cv2
import numpy as np
import const
import utils_MOT
import os
import measure
from kalman import Kalman
from pathlib import Path


# path:原视频
# path1:yolo检测得到的检测框坐标值txt文档存放地址
# path2:轨迹txt文件保存的地址

def mot(path, path1, path2):
    if not os.path.exists(str(path2)):
        os.mkdir(str(path2))
    del_file(path2)  # 清空文件
    # --------------------------------Kalman参数---------------------------------------
    # 状态转移矩阵，上一时刻的状态转移到当前时刻
    FILE = Path(__file__).resolve()
    A = np.array([[1, 0, 0, 0, 1, 0],
                  [0, 1, 0, 0, 0, 1],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0],
                  [0, 0, 0, 0, 1, 0],
                  [0, 0, 0, 0, 0, 1]])
    # 控制输入矩阵B
    B = None
    # 过程噪声协方差矩阵Q，p(w)~N(0,Q)，噪声来自真实世界中的不确定性,
    # 在跟踪任务当中，标移动的不确定性（突然加速、减速、转弯等）
    Q = np.eye(A.shape[0]) * 0.1
    # 状态观测矩阵
    H = np.array([[1, 0, 0, 0, 0, 0],
                  [0, 1, 0, 0, 0, 0],
                  [0, 0, 1, 0, 0, 0],
                  [0, 0, 0, 1, 0, 0]])
    # 观测噪声协方差矩阵R，p(v)~N(0,R)
    # 观测噪声来自于检测框丢失、重叠等
    R = np.eye(H.shape[0]) * 1
    # 状态估计协方差矩阵P初始化
    P = np.eye(A.shape[0])
    # ------------------------
    # 1.载入视频和目标位置信息
    # cap = cv2.VideoCapture(str(ROOT) + detect.OBJECT)  # 穿插着视频是为了方便展示
    cap = cv2.VideoCapture(str(path))  # 穿插着视频是为了方便展示
    frames_num = cap.get(7) # 获取视频帧数
    meas_list_all = measure.load_measurement(str(path1))
    # sz = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
    #       int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # opencv3.0
    # video_writer = cv2.VideoWriter(path3, fourcc, const.FPS, sz, True)
    # 2. 逐帧滤波
    state_list = []  # 单帧目标状态信息，存kalman对象
    frame_cnt = 1  # 帧数
    seen = 0  # 目标编号
    a = 1
    mea1 = []  # 暂存轨迹信息
    tracks_list_2 = []
    for meas_list_frame in meas_list_all:
        # --------------------------------------------加载当帧图像------------------------------------
        ret, frame = cap.read()
        if not ret:
            break

        # ---------------------------------------Kalman Filter for multi-objects-------------------
        # 预测
        for target in state_list:
            target.predict()
        # 关联
        mea_list = [utils_MOT.box2meas(mea) for mea in meas_list_frame]
        state_rem_list, mea_rem_list, match_list = Kalman.association(state_list, mea_list)
        # 状态没匹配上的，更新一下，如果触发终止就删除
        state_del = list()
        for idx in state_rem_list:
            status, _, _ = state_list[idx].update()
            if not status:
                state_del.append(idx)
        state_list = [state_list[i] for i in range(len(state_list)) if i not in state_del]
        # 量测没匹配上的，作为新生目标进行航迹起始
        for idx in mea_rem_list:
            state_list.append(Kalman(A, B, H, Q, R, utils_MOT.mea2state(mea_list[idx]), P))

        # -----------------------------------------------可视化-----------------------------------
        # 显示所有mea到图像上
        # for mea in meas_list_frame:
        #     cv2.rectangle(frame, tuple(mea[:2]), tuple(mea[2:]), const.COLOR_MEA, thickness=1)
        # 显示所有的state到图像上
        # for kalman in state_list:
        #     pos = utils_MOT.state2box(kalman.X_posterior)
        #     cv2.rectangle(frame, tuple(pos[:2]), tuple(pos[2:]), const.COLOR_STA, thickness=2)
        # 将匹配关系画出来
        # for item in match_list:
        #     cv2.line(frame, tuple(item[0][:2]), tuple(item[1][:2]), const.COLOR_MATCH, 3)
        # 绘制轨迹
        j = 0
        tracks_list_1 = []  # 储存上一帧的轨迹坐标信息
        for kalman in state_list:
            tracks_list = kalman.track

            # 1帧过后开始储存消失的物体之前的运动轨迹
            while frame_cnt > 1 and j < a and tracks_list[0] != tracks_list_2[j][0]:
                seen += 1
                cnt = frame_cnt - 1
                mea2 = []
                for i in range(len(tracks_list_2[j]) - 1, -1, -1):
                    with open(str(path2) + 'object' + str(seen) + '.txt', 'a') as f:
                        f.write(str(cnt))
                        f.write(' ')
                        f.write(str(seen))
                        f.write(' ')
                        f.write(str(tracks_list_2[j][i][0]))
                        f.write(' ')
                        f.write(str(tracks_list_2[j][i][1]))
                        f.write(' ')
                        f.write(str(tracks_list_2[j][i][2]))
                        f.write(' ')
                        f.write(str(tracks_list_2[j][i][3]))
                        f.write('\n')
                    mea2.append([cnt, seen, tracks_list_2[j][i][0], tracks_list_2[j][i][1], tracks_list_2[j][i][2],
                                 tracks_list_2[j][i][3]])
                    cnt -= 1
                j += 1
                mea1.append(mea2)

            tracks_list_1.append(tracks_list)
            j += 1
            a = len(tracks_list_2)  # 记录上一帧的目标个数

            if frame_cnt == frames_num:  # 视频播放到最后一帧时，记录所有轨迹
                cnt = frame_cnt
                seen += 1
                mea2 = []
                for i in range(len(tracks_list) - 1, -1, -1):
                    with open(path2 + 'object' + str(seen) + '.txt', 'a') as f:
                        f.write(str(cnt))
                        f.write(' ')
                        f.write(str(seen))
                        f.write(' ')
                        f.write(str(tracks_list[i][0]))
                        f.write(' ')
                        f.write(str(tracks_list[i][1]))
                        f.write(' ')
                        f.write(str(tracks_list[i][2]))
                        f.write(' ')
                        f.write(str(tracks_list[i][3]))
                        f.write('\n')
                    mea2.append([cnt, seen, tracks_list[i][0], tracks_list[i][1], tracks_list[i][2],
                                 tracks_list[i][3]])
                    cnt -= 1
                mea1.append(mea2)

            # for idx in range(len(tracks_list) - 1):  # tracks_list为每个bbox的中间坐标值
            #     # print(tracks_list)
            #     x1 = int((tracks_list[idx][0] + tracks_list[idx][2]) / 2)
            #     y1 = int((tracks_list[idx][1] + tracks_list[idx][3]) / 2)
            #     x2 = int((tracks_list[idx + 1][0] + tracks_list[idx][2]) / 2)
            #     y2 = int((tracks_list[idx + 1][1] + tracks_list[idx + 1][3]) / 2)
            #     cv2.line(frame, (x1, y1), (x2, y2), kalman.track_color, 4)
        # cv2.putText(frame, str(frame_cnt), (0, 50), color=const.RED, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5)
        # cv2.namedWindow('Demo', 0)
        # cv2.imshow('Demo', frame)
        # k = cv2.waitKey(0)  # 显示 1000 ms 即 1s 后消失
        # if k == 27:
        #     break
        frame_cnt += 1
        tracks_list_2 = tracks_list_1

    for mea_1 in mea1:
        for mea in mea_1:
            with open(path2 + 'mot.txt', 'a') as a:
                a.write(str(mea[0]))
                a.write(' ')
                a.write(str(mea[1]))
                a.write(' ')
                a.write(str(mea[2]))
                a.write(' ')
                a.write(str(mea[3]))
                a.write(' ')
                a.write(str(mea[4]))
                a.write(' ')
                a.write(str(mea[5]))
                a.write('\n')
    #
    # cap.release()
    # cap.release()
    # cv2.destroyAllWindows()


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


if __name__ == "__main__":
    import sys
    # mot(str(sys.argv[1]))
    # mot('/home/homefun/code/auto/minio_server/video/1057336131059751/DJI_20220714130355_0030_W.MP4',
    #     '/home/homefun/code/auto/minio_server/txt/1057336131059751/',
    #     '/home/homefun/code/auto/minio_server/mottxt/1057336131059751/')
    mot(sys.argv[1], sys.argv[2], sys.argv[3])
