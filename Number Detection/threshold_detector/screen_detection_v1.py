from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

cap = cv2.VideoCapture(0)

while True:
# load the example image
	ret, image = cap.read()
# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
	image = imutils.resize(image, height=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (7,7), 0)
	edged = cv2.Canny(blurred, 50, 200, 255) 

	cv2.imshow("edged",edged)
	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()

cv2.destroyAllWindows()