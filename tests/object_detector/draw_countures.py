import cv2
image = cv2.imread('calibration_point.jpg')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
thresholded = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]
contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
cv2.imshow('Detected Cards', image)
cv2.waitKey(0)
cv2.destroyAllWindows()