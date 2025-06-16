import cv2
import glob
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage

class TracerThread(QThread):
    ImageUpdate = Signal(QImage)
    PositionUpdate = Signal(tuple)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.snaps = []
        self.roi = None
        self.tracker = cv2.TrackerCSRT.create()
        self.active = True
        self.current_frame = None

    def setup(self, folder_path):
        """Настройка трекера с изображениями из указанной папки"""
        pathname = f"{folder_path}/*.jpg"
        self.snaps = sorted(glob.glob(pathname))
        if not self.snaps:
            return False
            
        # Загрузка первого кадра для инициализации трекера
        first_frame = cv2.imread(self.snaps[0])
        self.current_frame = first_frame.copy()
        
        # Показ ROI выбора
        roi = cv2.selectROI("Particle selection", first_frame, False)
        cv2.destroyWindow("Particle selection")
        # Обработка ROI

        if roi != (0, 0, 0, 0):
            self.roi = roi
            self.tracker.init(first_frame, roi)
            return True
        return False

    def run(self):
        """Основной цикл трекинга"""
        if not self.snaps or not self.roi:
            return
            
        for i in range(1, len(self.snaps)):
            if not self.active:
                break
                
            frame = cv2.imread(self.snaps[i])
            if frame is None:
                break
                
            self.current_frame = frame.copy()
            success, roi = self.tracker.update(frame)
            
            if success:
                # Рисуем метку на частице
                x, y, w, h = [int(v) for v in roi]
                position = (x + w // 2, y + h // 2)
                radius = ((w + h) // 7)
                cv2.circle(frame, position, radius, (0, 0, 255), 2)
                
                # Отправляем данные в основной поток
                self.PositionUpdate.emit(position)
            else:
                self.PositionUpdate.emit((-1, -1))  # Трекинг потерян
            
            # Конвертируем в QImage для отображения
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            self.ImageUpdate.emit(qt_image)

    def stop(self):
        """Остановка трекинга"""
        self.active = False