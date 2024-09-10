# 这些代码会在后面的程序中反复调用，不再说明
import numpy as np
import time
import matplotlib.pyplot as plt
import cupy as cp
import cv2 as cv
from matplotlib import animation

#改编自https://blog.csdn.net/m0_37816922/article/details/121880410
#改编自https://zhuanlan.zhihu.com/p/32703267

#生成z坐标 x0,y0 为起始点， nx,ny为点数， delta为点距
def genZ(x0, y0, nx, ny, delta):
    real, img = cp.indices([nx,ny])*delta
    real += x0
    img += y0
    return real.T+img.T*1j

#获取Newton集，n为迭代次数，m为判定发散点，大于1即可
def getJulia(z,c,n,m=2):
    t = time.time()
    for i in range(n):
        #牛顿迭代法
        #z = z - f(x) / f'(x)
        z = z - (c * (z ** 7) - c * z * z + 1) / (c * 7 * (z ** 6)  - 2 * c * z)
    out = cp.angle(z) / 6.28318530 * 255
    #print("time:",time.time()-t)
    return out

z1 = genZ(-2.5,-1.5,1500,1000,0.003)
fig = plt.figure()
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
ax = plt.subplot()

fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv.VideoWriter("NewtonGpu.mp4", fourcc, 30, (1500, 1000))  # 创建一个写入视频对象

mBrots = []
for y in np.arange(-1.5,1.5,0.2):
    for x in np.arange(-1.5,1.5,0.02):
        c = x + y*1j

        #输出灰度图转为RGB
        out = getJulia(z1,c,50)
        newton_out = cv.cvtColor(out.get().astype(np.uint8), cv.COLOR_GRAY2BGR)
        newton_out[:, :, 2] = newton_out[:, :, 2] / 10

        #添加文字
        text_str = 'f(z) = c * (z ** 7) - c * z * z + 1'
        cv.putText(newton_out, text_str, (0, 930), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)
        text_str = 'c = ' + str(round(x, 4)) + ' + ' + str(round(y, 4)) + '*1j' 
        cv.putText(newton_out, text_str, (0, 980), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)

        #将图片添加到视频流中
        videowriter.write(newton_out)
    
        print(c)

videowriter.release()



