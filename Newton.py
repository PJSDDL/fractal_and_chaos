import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import cv2 as cv

#改编自https://zhuanlan.zhihu.com/p/32703267
#牛顿分形

#取色板，用于给根上色
def color(ind, level):
    """每种颜色用RGB值表示: (R, G, B),
    level是灰度，收敛所用的迭代次数"""
    colors = [(180, 0, 30), (0, 180, 30), (0, 30, 180),
              (0, 190, 180), (180, 0, 175), (180, 255, 0),
              (155, 170, 180), (70, 50, 0),
              (150, 60, 0), (0, 150, 60), (0, 60, 150),
              (60, 150, 0), (60, 0, 150), (150, 0, 60),
              (130, 80, 0), (80, 130, 0), (130, 0, 80),
              (80, 0, 130), (0, 130, 80), (0, 80, 130),
              (110, 100, 0), (100, 110, 0), (0, 110, 100),
              (0, 100, 100), (110, 0, 100), (100, 0, 110),
              (255, 255, 255)]
    if ind < len(colors):
        c = colors[ind]
    else:
        c = (ind % 4 * 4, ind % 8 * 8, ind % 16 * 16)
    if max(c) < 210:
        c0 = c[0] + level
        c1 = c[1] + level
        c2 = c[2] + level
        return (c0, c1, c2)
    else:
        return c

def draw(f, df, n, size, name, x_min=-2.0, x_max=2., y_min=-2.0, y_max=2.0, eps=1e-3,
         max_iter=40):
    '''Given function f, its derivative df,
    generate its newton fractal with size, save to image with name
    f是一个函数，我们需要求解方程 f(x) = 0
    df是f的导数
    n是一个系数，用于调节分形形状
    size是图片大小,单位是像素
    name是保存图像的名字
    x_min, x_max, y_min, y_max定义了迭代初始值的取值范围
    eps是判断迭代停止的条件
    '''

    #牛顿迭代法
    def newton_method(c):
        "c is a complex number"
        for i in range(max_iter):
            c2 = c - f(c, n) / df(c, n)
            if abs(f(c, n)) > 1e10:
                return None, None
            if abs(c2 - c) < eps:
                return c2, i
            c = c2

        return None, None

    roots = [] # 记录所有根
    img = Image.new("RGB", (size, size)) # 把绘画结果保存为图片
    for x in range(size):
        for y in range(size): # 嵌套循环，遍历定义域中每个点，求收敛的根
            z_x = x * (x_max - x_min) / (size - 1) + x_min
            z_y = y * (y_max - y_min) / (size - 1) + y_min

            root, n_converge = newton_method(complex(z_x, z_y))
            if root:
                cached_root = False
                for r in roots:
                    if abs(r - root) < 1e-4: # 判断是不是已遇到过此根
                        root = r
                        cached_root = True
                        break
                if not cached_root:
                    roots.append(root)

            if root:
                img.putpixel((x, y), color(roots.index(root), n_converge)) # 上色
    print(roots) # 打印所有根
    return img

#牛队迭代法中的函数与导函数
def f(x, n):
    return n * x ** 3 - 1
def df(x, n):
    return n * 3 * x * x

#生成视频
fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
size = 1000
videowriter = cv.VideoWriter("Newton.mp4", fourcc, 30, (size, size))  # 创建一个写入视频对象

for i in np.arange(1, 10, 1):
    img = draw(f, df, i, size, "x^3-1.png")
    videowriter.write(np.array(img))

videowriter.release()