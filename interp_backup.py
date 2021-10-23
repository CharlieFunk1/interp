# importing libraries
import cv2
import numpy as np
from modules import Rgbstrip
import time
from ws4py.client.threadedclient import WebSocketClient

#Sets ip address of esp8266
esp8266host = "ws://192.168.0.159:81/"


# Number of pixels in strip
num_pixels = 106
# Starting position of strip, first led. (Canvas is 1600x900)
start_pos = [6,180]
# angle of strip
# TODO fix angle equations (possibly only for draw but check draw_strip and set_strip)
angle = 0
# length of led strip
length = 600 
# Create a regstrip object.  Equal to one rgb led strip.
rgbstrip = Rgbstrip(num_pixels, start_pos, angle, length)
# Canvas size (Video resolution for now)
#TODO: Increase canvas size to hd and have video play in it
canvas = (640, 360)

#Define websockets class
class Ledclient(WebSocketClient):
    def opened(self):
        print("Websocket open")
    def closed(self, code, reason=None):
        print("Connexion closed down", code, reason)
    def received_message(self, m):
        print(m)

        
#Create websocket
ws = Ledclient(esp8266host)
ws.connect()
print("Ready !")

# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/clines360p.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video  file")

# Read until video is completed
while(cap.isOpened()):

    print("FRAME ==================================================")
# Capture frame-by-frame
    ret, frame = cap.read()

    print("PIXEL ==================================================")
    # rgbstrip - get rgb values for all leds in strip using get
    
    for i in range(num_pixels):
        current_led = rgbstrip.get_rgb(frame, num_pixels, i)
        #pack the payload to be sent in websocket and send it
        payload = f"{current_led[0]}:{current_led[1]};{current_led[2]}." + str(i)
        #print(payload)

        #ws.send(payload)
        #give the payload some time.  May delete if all goes well.
        #time.sleep(1.10)
        #print(current_led)
    
    print("VIDEO ==================================================")
    if ret == True:

        # Display the resulting frame
        cv2.imshow('Frame', rgbstrip.draw_strip(frame, start_pos, angle, length))

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else: 
        print("BREAK ==================================================")
        break

#Close websocket connection
ws.close()
# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()


