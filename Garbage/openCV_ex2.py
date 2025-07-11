import cv2


def imageDrawContours(img):
    '''Возвращает изображение с контурами и контуры'''
    # CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=3., tileGridSize=(9,9))
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)  # convert from BGR to LAB color space
    l, a, b = cv2.split(lab)  # split on 3 different channels
    lab = cv2.merge((clahe.apply(l),a,b))  # merge channels
    img2 = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.cvtColor(lab, cv2.COLOR_LAB2BGR), cv2.COLOR_BGR2GRAY), (5, 5), 0), 110, 255, cv2.THRESH_BINARY)[1]
    contours = cv2.findContours(img2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0][:-1]
    cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
    
    return [img, contours]

def findPosition(cnts, old_pos):
    '''Находит позицию контура, включающего точку'''
    for cnt in cnts:
        (x,y),radius = cv2.minEnclosingCircle(cnt)
        print(x,y,radius)
        if x - radius < old_pos[0] and x + radius > old_pos[0] and y - radius < old_pos[1] and y + radius > old_pos[1]:
            return [[x,y], radius]
    print(old_pos)
    raise Exception('BadPosition!')

def findPair(img, pos, radius):
    x1 = int(pos[0] - radius*6)
    x2 = int(pos[0] + radius*6)
    y1 = int(pos[1] - radius*6)
    y2 = int(pos[1] + radius*6)
    sector = img[x1:x2, y1:y2] #Выделяем область поиска
    img, contours = imageDrawContours(sector)
    cv2.imshow('Image', img)
    cv2.waitKey(2000)
    cv2.destroyAllWindows()
    new_pos, new_radius = findPosition(contours, [radius*6, radius*6])
    new_pos[0] += pos[0] - radius*3
    new_pos[1] += pos[1] - radius*3
    if new_radius >= radius * 2: #Если частицы 'слиплись'
        new_pos[0] -= (radius + new_radius) * 0.71
        new_pos[1] -= (radius + new_radius) * 0.71
    return [img, new_pos, new_radius]


Trace = []

prefix = 'dataset/snap000'
img = cv2.imread('dataset/snap0001.jpg',1)[20:-20, 20:-20]
img, contours = imageDrawContours(img)
pos, radius = findPosition(contours,[300,300])
Trace.append(pos)

for i in range(8):
    path = prefix + str(2 + i) + '.jpg'
    img = cv2.imread(path)[20:-20, 20:-20]
    img, pos, radius = findPair(img, pos, radius)
    cv2.imshow('Image', img)
    cv2.waitKey(10)
    cv2.destroyAllWindows()
    
print(Trace)
print(radius)
