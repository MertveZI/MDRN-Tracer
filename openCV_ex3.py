import cv2
import glob

#Формирование списка с кадрами
pathname = 'C:/Users/mdrn/Documents/GitHub/MDRN-Tracer/dataset2/*.jpg'
snaps = glob.glob(pathname)


tracker = cv2.TrackerCSRT.create()
frame = cv2.imread(snaps[0],1)[20:-20, 20:-20]

# Выбор объекта для трекинга
bbox = cv2.selectROI("Select Object", frame, False)
cv2.destroyWindow("Select Object")



tracker.init(frame, bbox)
i=1
length = len(snaps) - 1
while True:
    frame = cv2.imread(snaps[i],1)[20:-20, 20:-20]
    i+=1
    
    success, bbox = tracker.update(frame)
    
    # Отрисовка прямоугольника
    if success:
        x, y, w, h = [int(v) for v in bbox]
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
        
        # Вывод координат
        print(f"p1: {p1}, p2: {p2}")
    
    cv2.imshow("Tracking", frame)
    
    # Выход по ESC
    k = cv2.waitKey(10) & 0xff
    if k == 27 or i> length:
        break

# Освобождение ресурсов
cv2.destroyAllWindows()