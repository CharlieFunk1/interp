# importing libraries
import cv2
import numpy as np
from modules import Getrgb
import serial
import time

ser = serial.Serial(
    port='/dev/ttyACM0',
    baudrate=115200,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

# Number of pixels in strip
num_pixels = 106
# Horizontal resolution of video
video_horiz_rez = 480


# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/clines360p.mp4')
   
# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video  file")
   
# Read until video is completed
while(cap.isOpened()):
      
  # Capture frame-by-frame
    ret, frame = cap.read()
        #print("DIR FRAME")
        #for i in dir(frame):
        #print(f"{i}: {getattr(frame, i)}")
    if ret == True:
         
        # Display the resulting frame
        cv2.imshow('Frame', frame)

        getrgb = Getrgb()
        # getrgb.frame = frame

        ser.write(b'!')

        for i in range(num_pixels - 1):
            pixel = getrgb.get(frame, num_pixels, video_horiz_rez, i)
            print(pixel)
            #ser.write(b'<')
            #ser.write(pixel[0])
            #ser.write(pixel[1])
            #ser.write(pixel[2])
            #ser.write(b'>')
            print("I ARE AM PIKSEL")
            #print(f" PIXEL IS :: {getrgb.get(frame, num_pixels, video_horiz_rez, i)}")

        print("NO MOAR PICKSELLL")
        
        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
     
    # Break the loop
    else: 
        print("CAP READ RETURMED FUCKOFF")
        break

ser.close()

# When everything done, release 
# the video capture object
cap.release()
   
# Closes all the frames
cv2.destroyAllWindows()
