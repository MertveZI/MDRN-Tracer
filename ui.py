from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QFileDialog, QHBoxLayout, QPushButton, QStatusBar
)
from PySide6.QtCore import Qt, QThread, Signal
from tracer import TracerThread
from collections import deque
import time

class FileWriterThread(QThread):
    """Поток для записи координат в файл"""
    finished = Signal()
    
    def __init__(self, buffer, filename):
        super().__init__()
        self.buffer = buffer
        self.filename = filename
        self.running = True
        
    def run(self):
        """Основной цикл записи"""
        try:
            with open(self.filename, 'a') as f:
                f.write("X,Y\n")  # Заголовок CSV
                while self.running or self.buffer:
                    if self.buffer:
                        x, y = self.buffer.popleft()
                        f.write(f"{x},{y}\n")
                        f.flush()  # Сброс буфера после каждой записи
                    self.msleep(5)  
        except Exception as e:
            print(f"Error writing to file: {e}")
        finally:
            self.finished.emit()
            
    def stop(self):
        """Остановка потока записи"""
        self.running = False

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MDRN_Tracer")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(100, 100, 600, 400)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout для центрального виджета
        self.VBL = QVBoxLayout(central_widget)
        
        # Label для отображения изображений
        self.FeedLabel = QLabel()
        self.FeedLabel.setAlignment(Qt.AlignCenter)
        self.VBL.addWidget(self.FeedLabel)
        
        # Кнопки управления
        self.ControlLayout = QHBoxLayout()
        
        self.OpenFolderBTN = QPushButton("Open Folder")
        self.OpenFolderBTN.clicked.connect(self.OpenFolder)
        self.ControlLayout.addWidget(self.OpenFolderBTN)
        
        self.StartBTN = QPushButton("Start Tracking")
        self.StartBTN.clicked.connect(self.StartTracking)
        self.StartBTN.setEnabled(False)
        self.ControlLayout.addWidget(self.StartBTN)
        
        self.CancelBTN = QPushButton("Stop")
        self.CancelBTN.clicked.connect(self.StopTracking)
        self.CancelBTN.setEnabled(False)
        self.ControlLayout.addWidget(self.CancelBTN)
        
        self.VBL.addLayout(self.ControlLayout)
        
        # Создаем статус бар
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Select folder with images to start")
        
        # Инициализация трекера
        self.Tracker = TracerThread()
        self.Tracker.ImageUpdate.connect(self.UpdateImage)
        self.Tracker.PositionUpdate.connect(self.UpdatePosition)
        
        # Буфер для координат
        self.coord_buffer = deque()
        self.frame_counter = 0
        self.writer_thread = None

    def OpenFolder(self):
        """Выбор папки с изображениями"""
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            success = self.Tracker.setup(folder)
            if success:
                self.statusBar.showMessage(f"Loaded {len(self.Tracker.snaps)} images. Select particle and press Start")
                self.StartBTN.setEnabled(True)
                
                # Сбрасываем счетчик кадров
                self.frame_counter = 0
            else:
                self.statusBar.showMessage("No images found or selection canceled")

    def StartTracking(self):
        """Запуск трекинга"""
        # Создаем уникальное имя файла с временной меткой
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        self.output_file = f"tracking_data_{timestamp}.csv"
        
        # Очищаем буфер
        self.coord_buffer.clear()
        self.frame_counter = 0
        
        # Запускаем поток записи
        self.writer_thread = FileWriterThread(self.coord_buffer, self.output_file)
        self.writer_thread.start()
        
        # Запускаем трекинг
        self.Tracker.active = True
        self.Tracker.start()
        self.StartBTN.setEnabled(False)
        self.CancelBTN.setEnabled(True)
        self.statusBar.showMessage(f"Tracking started. Saving to: {self.output_file}")

    def StopTracking(self):
        """Остановка трекинга"""
        # Останавливаем трекинг
        self.Tracker.stop()
        
        # Останавливаем поток записи
        if self.writer_thread:
            self.writer_thread.stop()
            self.writer_thread.quit()
            self.writer_thread.wait()
            self.writer_thread = None
        
        self.StartBTN.setEnabled(True)
        self.CancelBTN.setEnabled(False)
        self.statusBar.showMessage(f"Tracking stopped. Data saved to: {self.output_file}")

    def UpdateImage(self, Image):
        """Обновление изображения в интерфейсе"""
        pixmap = QPixmap.fromImage(Image)
        self.FeedLabel.setPixmap(pixmap.scaled(
            self.FeedLabel.width(), 
            self.FeedLabel.height(),
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        ))

    def UpdatePosition(self, position):
        """Обновление позиции частицы"""
        if position == (-1, -1):
            self.statusBar.showMessage("Tracking lost!")
        else:
            self.statusBar.showMessage(f"Position: X={position[0]}, Y={position[1]}")
            
            # Добавляем координаты в буфер
            self.frame_counter += 1
            self.coord_buffer.append((position[0], position[1]))