import cv2
import imutils
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

#from skimage.measure import compare_ssim

#Load the two images (city)

img1 = cv2.imread("images/ab.jpg") 
img1 = cv2.resize(img1, (600,360))
img2 =cv2.imread("images/ab1.jpg")
img2 = cv2.resize(img2, (600,360))

#Grayscale
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

#Find the difference between the two images 
#compue the mean structural similarity index

(similar , diff) = compare_ssim(gray1,gray2, full=True)

#diff is in range [0,1].convert it in range [0,255]
diff = (diff*255).astype("uint8")
cv2.imshow("Difference" , diff)

#Apply threshold
thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU) [1]

#cv2.imshow("Threshold", thresh)


#Find contours
contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = imutils.grab_contours(contours)

#Loop over each contour

for contour in contours:
   if cv2.contourArea(contour) > 100:
   # Calculate bounding box
     x, y, w, h= cv2.boundingRect(contour)
    # Draw rectangle bounding box
     cv2.rectangle(img1, (x,y), (x+w, y+h), (0,0,255), 2)
     cv2.rectangle(img2, (x,y), (x+w, y+h), (0,0,255), 2)
     
     cv2.putText(img2, "Similarity: " + str(similar),(10,30),cv2.FONT_HERSHEY_SIMPLEX, .7,(0,0,255),2)

# Show final images with differences 
x = np.zeros((360,10,3), np.uint8)
result = np.hstack((img1, x, img2)) 
cv2.imshow("Differences", result)

cv2.waitKey(0) 
cv2.destroyAllWindows()   