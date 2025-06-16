import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from ui import MainWindow

if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setStyle("Fusion")  # Установка темной темы
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())