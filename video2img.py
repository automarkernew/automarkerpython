import cv2
import os


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


def get_video_duration(filename):
    cap = cv2.VideoCapture(filename)
    if cap.isOpened():
        rate = cap.get(5)
        frame_num = cap.get(7)
        duration = frame_num / rate
        return duration
    return -1


def video2img(video, images):
    if not os.path.exists(images):
        os.mkdir(images)
    del_file(images)  # 保存帧图片前先清空文件夹

    cap = cv2.VideoCapture(video)  # 视频位置
    c = 1
    init_once = True
    while 1:
        success, frame = cap.read()
        if init_once:
            init_once = False
            size = frame.shape
            t = get_video_duration(video)
            with open(images + 'size.txt', 'a') as f:
                f.write(str(t))
                f.write(' ')
                f.write(str(size[0]))
                f.write(' ')
                f.write(str(size[1]))
                f.write(' ')
                # f.write('\n')
        if success:
            cv2.imwrite(images + str(c) + '.jpg', frame)
            c = c + 1
        else:
            break
    with open(images + 'size.txt', 'a') as f:
        f.write(str(c-1))
    cap.release()


if __name__ == '__main__':
    import sys
    # video2img('/home/hdtx/code/minio_server/video/901480240381958/rgb.jpg', '/home/hdtx/code/minio_server/motimg/901480240381958/')

    video2img(sys.argv[1], sys.argv[2])
