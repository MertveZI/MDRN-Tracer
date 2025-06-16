import cv2
import glob

def find_position(frame, tracker):
    '''Search for new position of particle'''
    success, roi = tracker.update(frame)
    # Отрисовка прямоугольника
    if success:
        x, y, w, h = [int(v) for v in roi]
        position = (x+(w//2), y+(h//2))
        radius =  ((w + h) // 7)
        cv2.circle(frame, position, radius, (0, 0, 255), 2)
    return position

#Формирование списка с кадрами
pathname = 'C:/Users/mdrn/Documents/GitHub/MDRN-Tracer/dataset3/vlad*.jpg'
snaps = glob.glob(pathname)
frame = cv2.imread(snaps[0],1)

# Инициализация трекера и области интереса
tracker = cv2.TrackerCSRT.create()
roi = cv2.selectROI("Particle selection", frame, False)
cv2.destroyWindow("Particle selection")
print(roi)
if roi != (0, 0, 0, 0):
    tracker.init(frame, roi)

    #Трекинг
    length = len(snaps) - 2
    i=0
    while True:
        i += 1
        frame = cv2.imread(snaps[i],1)
        x_pos, y_pos = find_position(frame,tracker)
        print(f"x: {x_pos}, y: {y_pos}")
        
        cv2.imshow("Tracking..", frame)
        
        # Выход по ESC
        k = cv2.waitKey(10) & 0xff
        if k == 27 or i> length:
            break

    # Освобождение ресурсов
    cv2.destroyAllWindows()
else:
    print('Tracking not started')