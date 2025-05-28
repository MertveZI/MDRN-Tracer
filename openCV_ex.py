#тест OpenCV инструментов

import cv2


path = 'bp_image.png'

def importImage(path):
    image = cv2.threshold(cv2.GaussianBlur(cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2GRAY), (5, 5), 0), 130, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('Image', image)

while True:
    importImage(path)
    key = cv2.waitKey(3000) & 0xFF
    if key == 27:
        cv2.destroyAllWindows()
        break   