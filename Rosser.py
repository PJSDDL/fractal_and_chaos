import numpy as np
import time
import matplotlib.pyplot as plt
import cv2 as cv
from matplotlib import animation

size = 1000
fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv.VideoWriter("Rosser.mp4", fourcc, 30, (size, size))  # 创建一个写入视频对象

for iter in np.arange(1,10,0.2):
    #微分方程起点
    x = 0
    y = 1
    z = 0

    #步长
    delta_t = 1e-3

    #微分方程系数
    w = 1.0
    a = 0.165
    b = 0.2
    c = iter 

    trace_x = [x]
    trace_y = [y]
    trace_z = [z]

    #差分方程代替微分
    for i in range(100000):
        trace_x.append((- w * trace_y[-1] - trace_z[-1]) * delta_t + trace_x[-1])
        trace_y.append((w * trace_x[-1] + a * trace_y[-1]) * delta_t + trace_y[-1])
        trace_z.append((b + (trace_x[-1] - c) * trace_z[-1]) * delta_t + trace_z[-1])

    #plt.plot(trace_x, trace_y)
    #plt.show()

    #归一化
    trace_x = np.array(trace_x)
    trace_y = np.array(trace_y) 
    trace_z = np.array(trace_z) 
    trace = np.vstack((trace_x,trace_y)).T
    trace = np.interp(trace, (trace.min(), trace.max()), (0, size))

    #绘制折线
    img = np.zeros((size, size, 3), dtype=np.uint8) + 255
    for point in trace:
        x = int(point[0])
        y = int(point[1])
        cv.circle(img, (x, y), 1, (0, 0, 0), 4)

    #添加文字
    text_str = 'w = ' + str(round(w, 4))
    cv.putText(img, text_str, (0, 830), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'a = ' + str(round(a, 4))
    cv.putText(img, text_str, (0, 880), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'b = ' + str(round(b, 4))
    cv.putText(img, text_str, (0, 930), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'c = ' + str(round(c, 4))
    cv.putText(img, text_str, (0, 980), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)

    for k in range(10):
        videowriter.write(img)

    print(iter)

videowriter.release()

