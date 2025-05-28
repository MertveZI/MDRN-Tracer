import cv2
def imageImport(path):
    image = cv2.imread(path)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()

print(imageImport('D:\Corvax.png'))
