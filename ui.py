from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, 
    QFileDialog, QHBoxLayout
)
from PySide6.QtCore import Qt
from tracer import TracerThread

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("MDRN_Tracer")
        self.setWindowIcon(QIcon('logo.png'))
        self.setGeometry(100, 100, 600, 400)
        
        # Основной layout
        self.VBL = QVBoxLayout()
        
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
        
        # Статус бар
        self.StatusLabel = QLabel("Select folder with images to start")
        self.VBL.addWidget(self.StatusLabel)
        
        # Инициализация трекера
        self.Tracker = TracerThread()
        self.Tracker.ImageUpdate.connect(self.UpdateImage)
        self.Tracker.PositionUpdate.connect(self.UpdatePosition)
        
        self.setLayout(self.VBL)

    def OpenFolder(self):
        """Выбор папки с изображениями"""
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            success = self.Tracker.setup(folder)
            if success:
                self.StatusLabel.setText(f"Loaded {len(self.Tracker.snaps)} images. Select particle and press Start")
                self.StartBTN.setEnabled(True)
            else:
                self.StatusLabel.setText("No images found or selection canceled")

    def StartTracking(self):
        """Запуск трекинга"""
        self.Tracker.active = True
        self.Tracker.start()
        self.StartBTN.setEnabled(False)
        self.CancelBTN.setEnabled(True)
        self.StatusLabel.setText("Tracking started...")

    def StopTracking(self):
        """Остановка трекинга"""
        self.Tracker.stop()
        self.StartBTN.setEnabled(True)
        self.CancelBTN.setEnabled(False)
        self.StatusLabel.setText("Tracking stopped")

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
            self.StatusLabel.setText("Tracking lost!")
        else:
            self.StatusLabel.setText(f"Position: X={position[0]}, Y={position[1]}")