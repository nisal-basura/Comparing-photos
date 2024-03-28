import cv2
import imutils
import numpy as np

#Load the two images (city)

img1 = cv2.imread("images/hen1.jpg") 
img1 = cv2.resize(img1, (600,360))
img2 =cv2.imread("images/hen2.jpg")
img2 = cv2.resize(img2, (600,360))

#Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#Find the difference between the two images using absdiff 
diff = cv2.absdiff(gray1, gray2) 
cv2.imshow("diff(img1, img2)", diff)

#Apply threshold
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) [1]

#cv2.imshow("Threshold", thresh)

#Dilation

kernel =  np.ones((5,5), np.uint8)
dilate =  cv2.dilate(thresh, kernel, iterations=2) 
cv2.imshow("Dilation", dilate)

#Find contours
contours = cv2.findContours(dilate.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

#Loop over each contour

for contour in contours:
   if cv2.contourArea(contour) > 100:
   # Calculate bounding box
     x, y, w, h= cv2.boundingRect(contour)
    # Draw rectangle bounding box
     cv2.rectangle(img1, (x,y), (x+w, y+h), (0,0,255), 2)
     cv2.rectangle(img2, (x,y), (x+w, y+h), (0,0,255), 2)

# Show final images with differences 
x = np.zeros((360,10,3), np.uint8)
result = np.hstack((img1, x, img2)) 
cv2.imshow("Differences", result)

#cv2.imshow("Original City", imgl)

#cv2.imshow("Edited", ing2)

cv2.waitKey(0) 
cv2.destroyAllWindows()