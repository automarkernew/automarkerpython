import cv2
import os
import re

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

#
def video2img2(video, images):
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

def video2img(video, images):
    if not os.path.exists(images):
        os.mkdir(images)
    del_file(images)  # 保存帧图片前先清空文件夹

    cap = cv2.VideoCapture(video)  # 视频位置
    c = 0
    i = 0
    init_once = True
    success, frame = cap.read()
    imgwith = 0
    imgheight = 0
    #10chou 1
    frame_rate = 10
    while success:
        i = i + 1
        if i % frame_rate == 0:
            c = c + 1
            cv2.imwrite(images + str(c) + '.jpg', frame)
            if init_once:
                init_once = False
                size = frame.shape
                imgwith = size[0]
                imgheight = size[1]
                t = get_video_duration(video)
                with open(images + 'size.txt', 'a') as f:
                    f.write(str(t))
                    f.write(' ')
                    f.write(str(size[0]))
                    f.write(' ')
                    f.write(str(size[1]))
                    f.write(' ')
                    # f.write('\n')
        success, frame = cap.read()
        # if success:
        #     cv2.imwrite(images + str(c) + '.jpg', frame)
        #     c = c + 1
        # else:
        #     break
    with open(images + 'size.txt', 'a') as f:
        f.write(str(c-1))
    cap.release()
    #img2video
    img2video(images, video, imgwith, imgheight)

def img2video(imgdir, videourl, imgwidth, imgheight):
    if os.path.exists(videourl):
        os.remove(videourl)
    head_tail = os.path.split(videourl)
    videoName = head_tail[1]
    videodir = head_tail[0]
    videotype = videoName.split('.')[1]
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    if videotype == "avi":
        fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    elif videotype == "flv":
        fourcc = cv2.VideoWriter_fourcc('f', 'l', 'v', '1')
    writer = cv2.VideoWriter(videourl,fourcc,25,(imgheight,imgwidth), True)
    total_frame = len(os.listdir(imgdir))
    for frame_num in range(total_frame):
        if frame_num != 0:
            img_path = imgdir + str(frame_num) + '.jpg'
            read_img = cv2.imread(img_path)
            writer.write(read_img)
    writer.release()


if __name__ == '__main__':
    import sys
    # video2img('/home/hdtx/code/minio_server/video/926848129171553/test1.flv', '/home/hdtx/code/minio_server/img/926848129171553/')
    if str(sys.argv[1])[-3:] == "mp4" or str(sys.argv[1])[-3:] == 'MP4':
        video2img(sys.argv[1], sys.argv[2])
    else:
        video2img2(sys.argv[1], sys.argv[2])

    # for test
    # argv = ['', '/home/homefun/code/project/minio_server/video/937783174627328/moon0713.jpg', '/home/homefun/code/project/minio_server/motimg/937783174627328/']
    # x = str(argv[1])[-3:] == "mp4" or 'MP4'
    # print(x)
    # if str(argv[1])[-3:] == "mp4" or 'MP4':
    #     video2img(argv[1], argv[2])
    # else:
    #     video2img2(argv[1], argv[2])
