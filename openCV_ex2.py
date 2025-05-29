import cv2


def imageDrawContours(img):
    '''Возвращает изображение с обрезанными углами и нарисованными контурами и контуры'''
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))
    lab = cv2.cvtColor(img[20:-20, 10:-20], cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    lab = cv2.merge((clahe.apply(l),a,b))  # merge channels
    img = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-15]
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    
    return [img, contours]

def findPosition(cnts, pos):
    '''Находит позицию контура, включающего точку'''
    for cnt in cnts:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        if x - radius < pos[0] and x + radius > pos[0] and y - radius < pos[1] and y + radius > pos[1]:
            return [(x,y), radius]
    raise Exception('BadPosition!')

def findPair(img, pos, radius):
    x1 = (pos[0] - radius*3)
    x2 = (pos[0] + radius*3)
    y1 = (pos[1] - radius*3)
    y2 = (pos[1] + radius*3)
    sector = img[x1:x2, y1:y2] #Выделяем область поиска
    img, contours = imageDrawContours(sector)
    new_pos, new_radius = findPosition(contours, pos)
    new_pos[0] += pos[0] - radius*3
    new_pos[1] += pos[1] - radius*3
    if new_radius >= radius * 2: #Если частицы 'слиплись'
        new_pos[0] -= (radius + new_radius) * 0.71
        new_pos[1] -= (radius + new_radius) * 0.71
    return [new_pos, new_radius]


Trace = []

prefix = 'dataset\snap'
img = cv2.imread('dataset\snap0001.jpg',1)
img, contours = imageDrawContours(img)
pos, radius = findPosition(contours,[300,300])
Trace.append(pos)

for i in range(8):
    path = prefix + '000' + str(2 + i) + '.jpg'
    img = cv2.imread(path ,1)
    img, contours = imageDrawContours(img)
    pos, radius = findPair(contours, pos, radius)
    cv2.imshow('Image', img)
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    
print(Trace)
print(radius)
