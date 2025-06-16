import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

        self.FeedLabel = QLabel()
        self.VBL.addWidget(self.FeedLabel)

        self.OpenFileBTN = QPushButton("open")
        self.VBL.addWidget(self.OpenFileBTN)


        self.setLayout(self.VBL)


    def file_open(self, path):
        """Открывает изображение или видео"""
        pass

    def image_analyze(self, image):
        """Открывает изображение"""
        pass

    def update_status(self, text, color):
        """Обновляет статус работы"""
        pass

    def update_image(self, image):
        """Обновление графиков с новыми данными."""
        pass

        


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Установка темной темы
    app.setStyle("Fusion")  
    dark_palette = QPalette()

    # Настройка палитры для темной темы
    dark_colors = {
        QPalette.Window: QColor(53, 53, 53),
        QPalette.WindowText: QColor(255, 255, 255),
        QPalette.Base: QColor(35, 35, 35),
        QPalette.AlternateBase: QColor(53, 53, 53),
        QPalette.ToolTipBase: QColor(255, 255, 255),
        QPalette.ToolTipText: QColor(255, 255, 255),
        QPalette.Text: QColor(255, 255, 255),
        QPalette.Button: QColor(53, 53, 53),
        QPalette.ButtonText: QColor(255, 255, 255),
        QPalette.BrightText: QColor(255, 0, 0),
        QPalette.Highlight: QColor(42, 130, 218),
        QPalette.HighlightedText: QColor(0, 0, 0),
    }

    for role, color in dark_colors.items():
        dark_palette.setColor(role, color)

    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())