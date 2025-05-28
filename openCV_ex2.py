import cv2

img = cv2.imread('bp_image.png',1)
# CLAHE (Contrast Limited Adaptive Histogram Equalization)
clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))

lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
l, a, b = cv2.split(lab)  # split on 3 different channels

l2 = clahe.apply(l)  # apply CLAHE to the L-channel

lab = cv2.merge((l2,a,b))  # merge channels
img2 = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)  # convert from LAB to BGR

image = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]

contours, _ = cv2.findContours(image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

cv2.imshow('Image', image)
cv2.waitKey(3000)
cv2.destroyAllWindows()