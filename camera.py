import cv2
import time
from test import detect_safe_search, detect_properties

# Windows dependencies
# - Python 2.7.6: http://www.python.org/download/
# - OpenCV: http://opencv.org/
# - Numpy -- get numpy from here because the official builds don't support x64:
#   http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy

# Mac Dependencies
# - brew install python
# - pip install numpy
# - brew tap homebrew/science
# - brew install opencv

cap = cv2.VideoCapture(0)
path = '/Users/Azula/Desktop/LAHACKS/ArkangelProject/capture.jpg'
while(True):

    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    cv2.imshow('frame', rgb)

    resize = cv2.resize(frame, (640, 480))
    out = cv2.imwrite('capture.jpg', resize, [int(cv2.IMWRITE_JPEG_QUALITY), 30])
    time.sleep(1)
    detect_safe_search(path)
    detect_properties(path)
    time.sleep(1)
        

cap.release()
cv2.destroyAllWindows()

