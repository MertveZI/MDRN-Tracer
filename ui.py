from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QFileDialog, QHBoxLayout, QPushButton, QStatusBar
)
from PySide6.QtCore import Qt
from tracer import TracerThread

class MainWindow(QMainWindow):  # Изменено на QMainWindow
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

    def OpenFolder(self):
        """Выбор папки с изображениями"""
        folder = QFileDialog.getExistingDirectory(self, "Select Image Folder")
        if folder:
            success = self.Tracker.setup(folder)
            if success:
                self.statusBar.showMessage(f"Loaded {len(self.Tracker.snaps)} images. Select particle and press Start")
                self.StartBTN.setEnabled(True)
            else:
                self.statusBar.showMessage("No images found or selection canceled")

    def StartTracking(self):
        """Запуск трекинга"""
        self.Tracker.active = True
        self.Tracker.start()
        self.StartBTN.setEnabled(False)
        self.CancelBTN.setEnabled(True)
        self.statusBar.showMessage("Tracking started...")

    def StopTracking(self):
        """Остановка трекинга"""
        self.Tracker.stop()
        self.StartBTN.setEnabled(True)
        self.CancelBTN.setEnabled(False)
        self.statusBar.showMessage("Tracking stopped")

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