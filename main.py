import sys
import threading
from PySide6 import QtWidgets, QtGui, QtCore
from views import AppUI
from PySide6.QtGui import QAction


class GraphApp(AppUI):
    def __init__(self):
        super().__init__()


    def image_open(self, path):
        """Открывает изображение"""
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

    def stop_image_parsing(self):
        """Останавливает парсинг изображений"""
        pass

    def start_image_parsing(self,count):
        """Начинает парсинг изображений"""
        for i in range(count):
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