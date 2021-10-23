# importing libraries
import cv2
import numpy as np
from modules import Rgbstrip
import time
import asyncio
import websockets
from websockets import connect
#TODO change payload to bits, try other network, send larger packets (strip)

#Sets ip address of modeMCU
esp8266host = "ws://192.168.0.159:81"

# Create a handler for the websocket connection. 
# from https://stackoverflow.com/questions/37369849/how-can-i-implement-asyncio-websockets-in-a-class
class EchoWebsocket:
    async def __aenter__(self):
        self._conn = connect(esp8266host)
        self.websocket = await self._conn.__aenter__()        
        return self

    async def __aexit__(self, *args, **kwargs):
        await self._conn.__aexit__(*args, **kwargs)

    # this is where the 'magic' happens
    async def send(self, message):
        await self.websocket.send(message)

    async def receive(self):
        return await self.websocket.recv()


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


# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video/clines360p.mp4')

# Check if camera opened successfully
if (cap.isOpened()== False): 
    print("Error opening video  file")

# all async calls MUST live in an async fn()
async def main():
    # In this context, we want an EchoWebSocket.  Let's call him 'echo'
    async with EchoWebsocket() as echo: 
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
                # even if it returns None, we must await async fn()s
                await echo.send(payload)


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

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
# When everything done, release 
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()


