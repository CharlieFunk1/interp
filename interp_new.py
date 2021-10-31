# importing libraries
import cv2
import numpy as np
from modules import Rgbstrip
import time
import websocket
#TODO change payload to bits, try other network, send larger packets (strip)

#Sets ip address of modeMCU
esp8266host = "ws://192.168.1.149:81"

# Number of pixels in strip
num_pixels = 106
# Starting position of strip, first led.  Grid starts in upper left.  As Y increases start point is further down (Canvas is 1920x1080)
start_pos = [50,50]
# angle of strip
# TODO fix angle equations (possibly only for draw but check draw_strip and set_strip)
angle = -28 * (-1)
# length of led strip
length = 1200 
# Create a regstrip object.  Equal to one rgb led strip.
rgbstrip = Rgbstrip(num_pixels, start_pos, angle, length)
# Canvas size (Video resolution for now)
#TODO: Increase canvas size to hd and have video play in it
canvas = (1920, 1080)

#Create websocket object
ws = websocket.WebSocket()

#Connect to websocket
ws.connect(esp8266host)

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/trip1280x720.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video  file")
    
            # Read until video is completed
    while(cap.isOpened()):
    
        print("FRAME ==================================================")
            # Capture frame-by-frame
        ret, frame = cap.read()
    
        print("SEND ==================================================")
    
            #pack the payload to be sent in websocket and send it
        payload = np.array(rgbstrip.get_rgb_strip(frame, num_pixels))
            #print(payload)
            #send payload
        ws.send(payload.tobytes())
    
    
        print("VIDEO ==================================================")
        if ret == True:
    
                # Display the resulting frame
            cv2.imshow('Frame', rgbstrip.draw_strip(frame, start_pos, angle, length))
    
                # Press Q on keyboard to  exit
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
    
        else:
            break
                    
# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

