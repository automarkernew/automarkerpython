import cv2
import sys
import os


def tracking(path1, path2, x1, y1, x2, y2, frame_start, frame_stop, frame_box, name):
    if not os.path.exists(str(path2)):
        os.mkdir(str(path2))
    # 创建跟踪器
    tracker1 = cv2.TrackerCSRT_create()
    tracker2 = cv2.TrackerCSRT_create()
    init_once = False
    init_twice = False
    # 读入视频
    video = cv2.VideoCapture(path1)
    # 读入第一帧
    ok, frame = video.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()
    # 存放帧图片
    img = []
    # 计算轨迹帧数

    frame_cnt = int(frame_box) - int(frame_start)
    # 框选bounding box

    x1 = float(x1)
    x2 = float(x2)
    y1 = float(y1)
    y2 = float(y2)
    boxes = (int(x1), int(y1), int(x2) - int(x1), int(y2) - int(y1))
    cnt = 0
    while True:
        cnt += 1
        ok, frame = video.read()
        if not ok or cnt > int(frame_stop):
            break
        # 保存目标帧
        if int(frame_box) >= cnt >= int(frame_start):
            img.append(frame)

        if not init_once and cnt == int(frame_box):
            tracker1.init(frame, boxes)
            # region = frame[bbox[1]: bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
            init_once = True

        if not init_twice and cnt == (int(frame_box)+1):
            tracker2.init(img[-1], boxes)
            # region = frame[bbox[1]: bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
            init_twice = True

        p1 = []
        p2 = []
        # 跟踪目标帧之前的帧
        if ok and init_once:
            for i in range(int(frame_cnt) + 1):
                ok, box = tracker1.update(img[-i - 1])
                cv2.rectangle(img[-i - 1], (int(box[0]), int(box[1])),
                              (int(box[0] + box[2]), int(box[1] + box[3])),
                              (255, 0, 0), 2, 1)
                p1.append((int(box[0]), int(box[1])))
                p2.append((int(box[0] + box[2]), int(box[1] + box[3])))
            for i in range(int(frame_cnt) + 1):
                with open(str(path2) + str(name) + '.txt', 'a') as f:
                    f.write(str(int(frame_start) + i))
                    f.write(' ')
                    f.write(str(p1[-i - 1][0]))
                    f.write(' ')
                    f.write(str(p1[-i - 1][1]))
                    f.write(' ')
                    f.write(str(p2[-i - 1][0]))
                    f.write(' ')
                    f.write(str(p2[-i - 1][1]))
                    f.write('\n')
            init_once = False
        # 跟踪目标帧之后的帧
        if ok and init_twice:
            ok, box = tracker2.update(frame)
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

            with open(str(path2) + str(name) + '.txt', 'a') as f:
                f.write(str(cnt))
                f.write(' ')
                f.write(str(p1[0]))
                f.write(' ')
                f.write(str(p1[1]))
                f.write(' ')
                f.write(str(p2[0]))
                f.write(' ')
                f.write(str(p2[1]))
                f.write('\n')
            # cv2.namedWindow('Tracking', 0)
            # cv2.imshow("Tracking", frame)
            # Exit
    #         k = cv2.waitKey(0) & 0xff
    #         if k == 27:
    #             break
    #
    # video.release()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    tracking(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
             sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8],
             sys.argv[9], sys.argv[10])
    # tracking('/home/hdtx/code/minio_server/video/898576699883520/5zhen.mp4',
    #          '/home/hdtx/code/minio_server/mottxt/898576699883520/', '587.9098138490656', '207.26893592447186',
    #          '698.3459231726033', '277.27704519712927', '2', '4',
    #          '3', 'object24')


