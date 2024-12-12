import cv2

# 读取彩色图像
image = cv2.imread('fish.jpg')
# 显示图像
cv2.imshow('Fish Image', image)
# 进行高斯滤波
blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
# 显示结果
cv2.imshow('Blurred Image', blurred_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
