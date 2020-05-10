
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
from PIL import ImageGrab

lower = np.array([0,0,0]) # lower limit of color in the mask
upper = np.array([45,45,45]) # upper limit of color in the mask

try:
    while(True):
        
        ''' preprocessing '''
        img = np.array(ImageGrab.grab(bbox=(25, 25, 640, 400))) #bbox specifies specific region (bbox= x,y,width,height)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # covert from BGR to RGB
        blur_mask = cv2.GaussianBlur(img, (5,5), 500, 100) # create a gaussian blur mask
        mask = cv2.inRange(blur_mask, lower, upper) # create a mask to remove background
        out = cv2.bitwise_and(img, img, mask=mask)   # apply the mask to the image
        img_edges = cv2.Canny(out, 100, 255) # canny edge detection
        img_mod, cnt, hierarchy = cv2.findContours(img_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # obtain contours

        
        ''' create approximate polynomial fit to the contours '''
        approx =[]
        for cnt in cnt:
            epsilon = 0.01*cv2.arcLength(cnt,True)
            app = cv2.approxPolyDP(cnt,epsilon,True)
            approx.append(app)
        

        ''' filter all the relevant contours --> the pot shape'''
        selectedContours = []
        for approx in approx:
            peri = cv2.arcLength(approx,True)
            area = cv2.contourArea(approx)
            
            try:
                compactness = ((peri * peri)/(4 * 3.14 * area))
            except:ZeroDivisionError
                            
            if compactness > 0.5 and compactness < 3.5 and area > 1000 and area < 1500:
                selectedContours.append(approx)
                
        for selectedContours in selectedContours:
            (x,y),radius = cv2.minEnclosingCircle(selectedContours)
            center = (int(x),int(y))
            radius = int(radius)
            if radius  < 40:
                cv2.circle(img,center,radius,(0,255,0),2)
                x,y = center
                cv2.putText(img,'Player',(x+30,y-50),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
                cv2.putText(img,'.',(x,y),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,255,0),5)
        
        cv2.imshow('contours', img) 
        cv2.waitKey(1)  

except KeyboardInterrupt:
    cv2.destroyAllWindows() 

