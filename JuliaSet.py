import numpy as np
import time
import matplotlib.pyplot as plt
import cupy as cp
import cv2 as cv
from matplotlib import animation

#改编自https://blog.csdn.net/m0_37816922/article/details/121880410

#生成z坐标 x0,y0 为起始点， nx,ny为点数， delta为点距
def genZ(x0, y0, nx, ny, delta):
    real, img = cp.indices([nx,ny])*delta
    real += x0
    img += y0
    return real.T+img.T*1j

#获取Julia集，n为迭代次数，m为判定发散点，大于1即可
def getJulia(z,c,n,m=2):
    t = time.time()
    z,out = z*1, cp.abs(z)
    c = cp.zeros_like(z)+c
    for i in range(n):
        absz = cp.abs(z)
        z[absz>m]=0		#对开始发散的点置零
        c[absz>m]=0		
        out[absz>m]=i*255/n	#记录发散点的发散速度
        z = z*z + c
    print("time:",time.time()-t)
    return out

z1 = genZ(-2.5,-1.5,1500,1000,0.003)
fig = plt.figure()
fig.subplots_adjust(top=1, bottom=0, left=0, right=1)
ax = plt.subplot()

fourcc = cv.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv.VideoWriter("Julia.mp4", fourcc, 30, (1500, 1000))  # 创建一个写入视频对象

mBrots = []
for y in np.arange(-1.5,1.5,0.1):
    for x in np.arange(-1.5,1.5,0.1):
        c = x + y*1j

        #输出灰度图转为RGB
        out = getJulia(z1,c,40)
        julia_out = cv.cvtColor(out.get().astype(np.uint8), cv.COLOR_GRAY2BGR)
        julia_out[:, :, 2] = julia_out[:, :, 2] / 10

        #添加文字
        text_str = 'c = ' + str(round(x, 4)) + ' + ' + str(round(y, 4)) + '*1j' 
        cv.putText(julia_out, text_str, (0, 980), cv.FONT_HERSHEY_SCRIPT_COMPLEX, 1.5, (102, 204, 255), 2)

        #保存gif帧
        '''
        im = ax.imshow(julia_out,cmap=plt.cm.jet, animated=True)
        ax.set_axis_off()
        mBrots.append([im])
        '''

        #将图片添加到视频流中
        videowriter.write(julia_out)
    print(y)

videowriter.release()

'''
ani = animation.ArtistAnimation(fig, mBrots, interval=1000)
plt.show()
ani.save('julia.gif',writer='imagemagick')
'''

