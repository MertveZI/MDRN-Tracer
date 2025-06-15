import cv2
import glob

def find_pair(frame, tracker):
    success, roi = tracker.update(frame)
    # Отрисовка прямоугольника
    if success:
        x, y, w, h = [int(v) for v in roi]
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
    return(p1,p2)
#Формирование списка с кадрами
pathname = 'C:/Users/mdrn/Documents/GitHub/MDRN-Tracer/dataset2/*.jpg'
snaps = glob.glob(pathname)
frame = cv2.imread(snaps[0],1)[20:-20, 20:-20]

# Инициализация трекера и области интереса
tracker = cv2.TrackerCSRT.create()
roi = cv2.selectROI("Select Object", frame, False)
cv2.destroyWindow("Select Object")
tracker.init(frame, roi)

#Трекинг
length = len(snaps) - 2
i=0
while True:
    i += 1
    frame = cv2.imread(snaps[i],1)[20:-20, 20:-20]
    p1,p2 = find_pair(frame,tracker)
    print(f"p1: {p1}, p2: {p2}")
    
    cv2.imshow("Tracking", frame)
    
    # Выход по ESC
    k = cv2.waitKey(10) & 0xff
    if k == 27 or i> length:
        break

# Освобождение ресурсов
cv2.destroyAllWindows()