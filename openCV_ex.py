import cv2
import glob

#Формирование списка с

path = 'voskres.mp4'
# Инициализация трекера и видеопотока
tracker = cv2.TrackerKCF.create()
video = cv2.VideoCapture(path)

# Чтение первого кадра
ret, frame = video.read()
if not ret:
    print("Ошибка чтения камеры!")
    exit()

# Выбор объекта для трекинга
bbox = cv2.selectROI("Select Object", frame, False)
cv2.destroyWindow("Select Object")

# Инициализация трекера
tracker.init(frame, bbox)

while True:
    # Чтение кадра
    ret, frame = video.read()
    if not ret:
        break
    
    # Обновление трекера
    success, bbox = tracker.update(frame)
    
    # Отрисовка прямоугольника при успешном трекинге
    if success:
        x, y, w, h = [int(v) for v in bbox]
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, (0, 0, 255), 2, 1)
        
        # Вывод координат (опционально)
        print(f"p1: {p1}, p2: {p2}")
    
    # Отображение результата
    cv2.imshow("Tracking", frame)
    
    # Выход по ESC
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

# Освобождение ресурсов
video.release()
cv2.destroyAllWindows()