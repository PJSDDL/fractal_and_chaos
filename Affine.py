import numpy as np
import matplotlib.pyplot as plt
import cv2

def my_warpAffine(img, pts1, pts2):
    cols,rows,ch = img.shape
    M1 = cv2.getAffineTransform(pts1, pts2)
    dst1 = cv2.warpAffine(img, M1, (cols,rows), borderValue=(255,255,255))
    dst1 = cv2.resize(dst1, (rows,cols))

    return dst1

def mask_add(img, dst1):
    #取掩膜
    img2gray = cv2.cvtColor(dst1,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 200, 255, cv2.THRESH_BINARY)
    #负掩膜
    mask_inv = cv2.bitwise_not(mask)
    #图像融合
    img1_bg = cv2.bitwise_and(dst1,dst1,mask = mask_inv)
    img2_fg = cv2.bitwise_and(img,img,mask = mask)

    return cv2.add(img1_bg,img2_fg)


img = cv2.imread('sddl.jpg')
cols,rows,ch = img.shape
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 用于mp4格式的生成
videowriter = cv2.VideoWriter("Affine.mp4", fourcc, 30, (rows,cols))  # 创建一个写入视频对象

for k in range(1,30*60,2):
    img = cv2.imread('sddl.jpg')
    cols,rows,ch = img.shape

    for i in range(1,20):
        pts1 = np.float32([[0,0],[1000,0],[0,1000]])
        pts2 = np.float32([[0,0],[500+k/18,0],[0,510-k/7]])  
        dst1 = my_warpAffine(img, pts1, pts2)

        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[1000,500+k/18],[1000-k/18,1000],[0,1000-k/18]])  
        dst2 = my_warpAffine(img, pts1, pts2)

        img = mask_add(img, dst1)
        img = mask_add(img, dst2)
    videowriter.write(img)
    print(k)

videowriter.release()
cv2.imshow("img", img)
cv2.waitKey(0)

'''
#道理之树
        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[0,0],[710+k/18,0],[710,710-k/7]])  
        dst1 = my_warpAffine(img, pts1, pts2)

        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[750,k/18],[750-k/18,750],[0,750-k/18]])  
        dst2 = my_warpAffine(img, pts1, pts2)
'''

'''
#道理雪花
        pts1 = np.float32([[0,0],[1000,0],[0,1000]])
        pts2 = np.float32([[0,0],[500+k/18,0],[0,510-k/7]])  
        dst1 = my_warpAffine(img, pts1, pts2)

        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[1000,0+k/18],[1000-k/18,1000],[0,1000-k/18]])  
        dst2 = my_warpAffine(img, pts1, pts2)
'''

'''
#纸piaji（东北土话，纸卡片）
        pts1 = np.float32([[0,0],[1000,0],[0,1000]])
        pts2 = np.float32([[0,0],[500+k/18,500],[500,510-k/7]])  
        dst1 = my_warpAffine(img, pts1, pts2)

        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[1000,200+k/18],[1000-k/18,1200],[0,1200-k/18]])  
        dst2 = my_warpAffine(img, pts1, pts2)
'''

'''
#怪诞树叶
        pts1 = np.float32([[0,0],[1000,0],[0,1000]])
        pts2 = np.float32([[0,0],[0,510-k/7],[500+k/9,0]])  
        dst1 = my_warpAffine(img, pts1, pts2)

        pts1 = np.float32([[0,0],[1000,0],[1000,1000]])
        pts2 = np.float32([[0,0+k/9],[1000-k/9,0],[800,1000-k/9]])  
        dst2 = my_warpAffine(img, pts1, pts2)
'''
