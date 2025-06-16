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

        self.CancelBTN = QPushButton("Cancel")
        self.CancelBTN.clicked.connect(self.CancelFeed)
        self.VBL.addWidget(self.CancelBTN)

        self.OpenFileBTN = QPushButton("open")
        self.VBL.addWidget(self.OpenFileBTN)

        self.ImageWindow = ImageWindow()

        self.ImageWindow.start()
        self.ImageWindow.ImageUpdate.connect(self.ImageUpdateSlot)
        self.setLayout(self.VBL)

    def ImageUpdateSlot(self, Image):
        self.FeedLabel.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.ImageWindow.stop()

class ImageWindow(QThread):
    ImageUpdate = Signal(QImage)
    def run(self):
        self.ThreadActive = True
        Capture = cv2.VideoCapture(0)
        while self.ThreadActive:
            ret, frame = Capture.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                Pic = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                self.ImageUpdate.emit(Pic)
    def stop(self):
        self.ThreadActive = False
        self.quit()

if __name__ == "__main__":
    App = QApplication(sys.argv)
    # Установка темной темы
    App.setStyle("Fusion")  
    Root = MainWindow()
    Root.show()
    sys.exit(App.exec())