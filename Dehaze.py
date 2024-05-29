import math
import time
import cv2
import numpy as np


def dark_channel(image):
    """
    计算暗通道图像
    :param image: 原图像
    :return: 暗通道灰度图
    """
    min_img = np.min(image, axis=2)
    dark_img = cv2.erode(min_img, cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15)))
    return dark_img


def guided_filter(I, p, win_size, eps):
    """
    导向滤波
    :param I: 导向图像，灰度图
    :param p: 输入图像，灰度图
    :param win_size: 滤波窗口大小
    :param eps: 平滑系数
    :return: 滤波后的图像
    """
    mean_I = cv2.boxFilter(I, cv2.CV_64F, win_size)
    mean_p = cv2.boxFilter(p, cv2.CV_64F, win_size)
    mean_Ip = cv2.boxFilter(I * p, cv2.CV_64F, win_size)
    mean_II = cv2.boxFilter(I * I, cv2.CV_64F, win_size)

    cov_Ip = mean_Ip - mean_I * mean_p
    var_I = mean_II - mean_I * mean_I

    a = cov_Ip / (var_I + eps)
    b = mean_p - a * mean_I

    mean_a = cv2.boxFilter(a, cv2.CV_64F, win_size)
    mean_b = cv2.boxFilter(b, cv2.CV_64F, win_size)

    q = mean_a * I + mean_b
    return q


def estimate_atmospheric_light(image, dark_img):
    """
    估计大气光值
    :param image: 原图像
    :param dark_img: 暗通道图像
    :return: 大气光值
    """
    flat_img = dark_img.ravel()
    flat_img_indices = flat_img.argsort()[::-1]
    top_indices = flat_img_indices[:max(math.floor(len(flat_img) / 1000), 1)]
    A = np.mean(image.reshape(-1, 3)[top_indices], axis=0)
    return A


def transmission_estimation(guided_img):
    """
    估计透射率
    :param guided_img: 引导图像
    :return: 透射率
    """
    return np.clip(1 - 0.95 * guided_img, 0.3, 1.0)


def dehaze(image):
    """
    图像去雾
    :param image: 原图像
    :return: 去雾后的图像
    """
    dark_img = dark_channel(image)
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) / 255.0
    guided_img = guided_filter(gray_img, dark_img / 255.0, (81, 81), 0.001)

    A = estimate_atmospheric_light(image, dark_img)
    tx = transmission_estimation(guided_img)

    J = (image - A) / tx[:, :, np.newaxis] + A
    return np.clip(J, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    path = r"D:\test_images\01.jpg"
    image = cv2.imread(path)
    resized_image = cv2.resize(image, (500, int(500 * image.shape[0] / image.shape[1])))
    
    dehazed_image = dehaze(resized_image)
    
    cv2.imshow('Dehaze', np.hstack((resized_image, dehazed_image)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
