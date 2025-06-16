import cv2


def imageDrawContours(img):
    '''Возвращает изображение с обрезанными краями и нарисованными контурами и контуры'''
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    lab = cv2.merge((clahe.apply(l),a,b))  # merge channels
    img = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-15]
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    
    return [img, contours]

img = cv2.imread('dataset/snap0001.jpg')
pos, radius = [300,300], 9 
sector = imageDrawContours(img)[0]
cv2.imshow('Image', sector)
cv2.waitKey(0)
cv2.destroyAllWindows()

x1 = int(pos[0] - radius*3)
x2 = int(pos[0] + radius*3)
y1 = int(pos[1] - radius*3)
y2 = int(pos[1] + radius*3)
sector = img[x1:x2, y1:y2] #Выделяем область поиска
cv2.imshow('Image', sector)
cv2.waitKey(0)
cv2.destroyAllWindows()
sector = imageDrawContours(sector)[0]
cv2.imshow('Image', sector)
cv2.waitKey(0)
cv2.destroyAllWindows()