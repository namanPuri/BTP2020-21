from imutils.perspective import four_point_transform
from imutils import contours
import imutils
import cv2

def bird_view(image):
	image = imutils.resize(image, height=500)
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	blurred = cv2.GaussianBlur(gray, (5,5), 0)
	edged = cv2.Canny(blurred, 200, 92, 255)

	cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)

	cnts = imutils.grab_contours(cnts)
	cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
	displayCnt = None

	# loop over the contours
	for c in cnts:
		# approximate the contour
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.02 * peri, True)
		# if the contour has four vertices, then we have found
		# the display
		if len(approx) == 4:
			displayCnt = approx
			break
	warped = four_point_transform(gray, displayCnt.reshape(4, 2))
	output = four_point_transform(image, displayCnt.reshape(4, 2))
	return warped, output

#dictionary defineD according to : 
# 	  __0__
#   1|	   |2
#    |__3__|	
#   4|	   |5
#    |__6__|
		  	
DIGITS_LOOKUP = {					#dictionary 
	(1, 1, 1, 0, 1, 1, 1): 0,		# tuple = key, ans = value
	(0, 0, 1, 0, 0, 1, 0): 1,
	(1, 0, 1, 1, 1, 1, 0): 2,
	(1, 0, 1, 1, 0, 1, 1): 3,
	(0, 1, 1, 1, 0, 1, 0): 4,
	(1, 1, 0, 1, 0, 1, 1): 5,
	(1, 1, 0, 1, 1, 1, 1): 6,
	(1, 0, 1, 0, 0, 1, 0): 7,
	(1, 1, 1, 1, 1, 1, 1): 8,
	(1, 1, 1, 1, 0, 1, 1): 9
}

# load the example image


#image = cv2.imread('..\\Images_to_test\\9.jpeg')
# pre-process the image by resizing it, converting it to
# graycale, blurring it, and computing an edge map
cap = cv2.VideoCapture(0)

while True:

	image = cap.read()[1]
	warped, output = bird_view(image)

	thresh = cv2.adaptiveThreshold(warped,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
				cv2.THRESH_BINARY_INV,11,2)

	#cv2.imshow("intial",thresh)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 3))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
	#cv2.imshow("afteropne",thresh)

	kernel2 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
	thresh = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel2)

	thresh = cv2.erode(thresh,kernel,iterations = 1)

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_TREE,
		cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)
	digitCnts = []

	# loop over the digit area candidates
	for c in cnts:
		# compute the bounding box of the contour
		(x, y, w, h) = cv2.boundingRect(c)
		# if the contour is sufficiently large, it must be a digit
		#cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
		if w >= 6 and (h >= 15 and h <= 30):
			digitCnts.append(c)
	#cv2.imshow("edged3",output)
	#cv2.imshow("edged2",thresh)
	for c in digitCnts:
		# extract the digit ROI
		(x, y, w, h) = cv2.boundingRect(c)
		if w < 8 and (h >15 and h < 30):
			x = x - 8
			w = w + 8
		roi = thresh[y:y + h, x:x + w]
		cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),1)
		cv2.rectangle(warped,(x,y),(x+w,y+h),(0,0,255),1)

	cv2.imshow("edged",output)
	cv2.imshow("thresh",thresh)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()



