import cv2
import numpy as np


camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
return_value, image = camera.read()

cv2.imwrite('images/img.png', image)

cv2.imshow('image', image)
    
# if cv2.waitKey(20) & 0xFF == ord('q'): 
# 	break

camera.release()
cv2.destroyAllWindows()