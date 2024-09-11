import numpy as np
import time
import matplotlib.pyplot as plt
import cv2 as cv
from matplotlib import animation

size = 1000
fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv.VideoWriter("Martin.mp4", fourcc, 30, (size, size))  # 创建一个写入视频对象

for iter in np.arange(1,100,0.1):
    #系数
    a = iter / 100
    b = 0.75
    c = 0.83

    trace_x = [1.0]
    trace_y = [1.0]

    #分形迭代
    for i in range(100000):
        y_temp = a - trace_x[-1]
        x_temp = trace_y[-1] - np.sign(trace_x[-1]) * np.sqrt(abs(b * trace_x[-1] - c))

        trace_y.append(y_temp)
        trace_x.append(x_temp)

    #归一化
    trace_x = np.array(trace_x)
    trace_y = np.array(trace_y) 
    trace = np.vstack((trace_x,trace_y)).T
    trace = np.interp(trace, (trace.min(), trace.max()), (0, size))

    #绘制折线
    img = np.zeros((size, size, 3), dtype=np.uint8) + 255
    for point in trace:
        x = int(point[0])
        y = int(point[1])
        cv.circle(img, (x, y), 1, (0, 0, 0), 4)

    #添加文字
    text_str = 'a = ' + str(round(a, 4))
    cv.putText(img, text_str, (0, 830), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'b = ' + str(round(b, 4))
    cv.putText(img, text_str, (0, 880), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
    text_str = 'c = ' + str(round(c, 4))
    cv.putText(img, text_str, (0, 930), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)

    videowriter.write(img)

    print(iter)

videowriter.release()

