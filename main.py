import sys
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
import cv2

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.VBL = QVBoxLayout()

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
    app = QtWidgets.QApplication(sys.argv)

    # Установка темной темы
    app.setStyle("Fusion")  # Используем стиль Fusion
    dark_palette = QtGui.QPalette()

    # Настройка палитры для темной темы
    dark_colors = {
        QtGui.QPalette.Window: QtGui.QColor(53, 53, 53),
        QtGui.QPalette.WindowText: QtGui.QColor(255, 255, 255),
        QtGui.QPalette.Base: QtGui.QColor(35, 35, 35),
        QtGui.QPalette.AlternateBase: QtGui.QColor(53, 53, 53),
        QtGui.QPalette.ToolTipBase: QtGui.QColor(255, 255, 255),
        QtGui.QPalette.ToolTipText: QtGui.QColor(255, 255, 255),
        QtGui.QPalette.Text: QtGui.QColor(255, 255, 255),
        QtGui.QPalette.Button: QtGui.QColor(53, 53, 53),
        QtGui.QPalette.ButtonText: QtGui.QColor(255, 255, 255),
        QtGui.QPalette.BrightText: QtGui.QColor(255, 0, 0),
        QtGui.QPalette.Highlight: QtGui.QColor(42, 130, 218),
        QtGui.QPalette.HighlightedText: QtGui.QColor(0, 0, 0),
    }

    for role, color in dark_colors.items():
        dark_palette.setColor(role, color)

    app.setPalette(dark_palette)

    window = GraphApp()
    window.show()
    sys.exit(app.exec())