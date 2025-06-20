import sys
from PySide6.QtWidgets import QApplication
from ui import MainWindow

if __name__ == "__main__":
    App = QApplication(sys.argv)
    App.setStyle("Fusion")  
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())