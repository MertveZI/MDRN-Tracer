import cv2


path = 'bp_image.png'

def imageDrawCountours(path):
    img = cv2.imread(path,1)
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    lab = cv2.merge((clahe.apply(l),a,b))  # merge channels
    image = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    
    return img

img = imageDrawCountours(path)
cv2.imshow('Image', img)
cv2.waitKey(3000)
cv2.destroyAllWindows()