import cv2


path = 'bp_image.png'

def imageDrawContours(path):
    '''Возвращает изображение с обрезанными углами и нарисованными контурами и контуры'''
    img = cv2.imread(path,1)[20:-20, 10:-20]
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    lab = cv2.merge((clahe.apply(l),a,b))  # merge channels
    image = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-15]
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    
    return img, contours

def findPosition(cnts, pos):
    for cnt in cnts:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        if x - radius < pos[0] and x + radius > pos[0] and y - radius < pos[1] and y + radius > pos[1]:
            return [x,y], radius
    raise Exception('BadPosition!')


img, contours = imageDrawContours(path)
print(findPosition(contours,[300,300]))
cv2.imshow('Image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()