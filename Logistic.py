import numpy as np
import time
import matplotlib.pyplot as plt
import cv2 as cv
from matplotlib import animation

size = 1000
fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv.VideoWriter("Logistic.mp4", fourcc, 30, (size, size))  # 创建一个写入视频对象

for iter in np.arange(3,4,0.0005):
    #系数
    w = 3.6
    y0 = iter

    trace_x = [0.1]
    trace_y = [y0]

    #差分方程代替微分
    for i in range(1000):
        trace_x.append(trace_x[-1] + 1)
        trace_y.append(trace_y[-1] * w * (1 - trace_y[-1]))

    #plt.plot(trace_x, trace_y)
    #plt.show()

    #归一化
    trace_x = np.array(trace_x)
    trace_y = np.array(trace_y) 
    trace_x = np.interp(trace_x, (trace_x.min(), trace_x.max()), (0, size))
    trace_y = np.interp(trace_y, (trace_y.min(), trace_y.max()), (0, size))
    trace = np.vstack((trace_x,trace_y)).T

    #绘制折线
    img = np.zeros((size, size, 3), dtype=np.uint8) + 255
    for point in trace:
        x = int(point[0])
        y = int(point[1])
        cv.circle(img, (x, y), 1, (0, 0, 0), 4)

    #添加文字
    text_str = 'w = ' + str(round(w, 4))
    cv.putText(img, text_str, (0, 830), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'y0 = ' + str(round(y0, 4))
    cv.putText(img, text_str, (0, 880), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'y = y * w * (1 - y)'
    cv.putText(img, text_str, (0, 930), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)

    videowriter.write(img)

    print(iter)

videowriter.release()

