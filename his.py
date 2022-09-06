# hdr_path为高光谱图像文件路径, 路径下需要遥感图像头文件'*.HDR'与相同文件名的高光谱图像文件
# save_path为生成伪彩色图片'rgb.jpg'与展示通道图片路径
# 高光谱图像数据处理模块
# pip install spectral
import spectral as spy
import numpy as np
# import matplotlib.pyplot as plt


def hdr2rgb(hdr_path, save_path):
    # data = spy.envi.open(hdr_path + '.HDR', hdr_path)
    # x = hdr_path.replace('.hdr', '')
    data = spy.envi.open(hdr_path, hdr_path.replace('.hdr', ''))
    ls = np.asarray(list(map(eval, data.metadata['wavelength'])))
    r_index = len(np.extract(ls < 655, ls))
    g_index = len(np.extract(ls < 563, ls))
    b_index = len(np.extract(ls < 482, ls))
    # view = spy.imshow(data, (r_index, g_index, b_index))
    # plt.show()
    spy.save_rgb(save_path + '1.jpg', data, [r_index, g_index, b_index])
    spy.save_rgb(save_path + '2.jpg', data, [r_index, r_index, r_index])
    spy.save_rgb(save_path + '3.jpg', data, [b_index, b_index, b_index])
    return


if __name__ == "__main__":
    import sys
    hdr2rgb(sys.argv[1], sys.argv[2])
    # hdr2rgb('/home/hdtx/code/minio_server/video/901480240381965/b0001.hdr', '/home/hdtx/code/minio_server/video/901480240381965/')