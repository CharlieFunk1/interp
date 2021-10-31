import cv2
import numpy as np
import math

class Rgbstrip:
    #initialize the object with starting position in array "strip" and run set_strip to add coordinates
    def __init__(self, num_pixels, start_pos, angle, length):
        self.strip = [(start_pos[0], start_pos[1])]
        self.set_strip(num_pixels, start_pos, angle, length)

    # Gets the RGB values from from frame for led (i) on the strip.  Returns (R,G,B)
    def get_rgb(self, frame, num_pixels, i):
        x = int(self.strip[i][0])  #int(((frame.shape[1]-1) / num_pixels) * i)
        y = int(self.strip[i][1])  #int((strip_hposition * .01) * frame.shape[0])
        try:
            pixel = [frame[y][x][2],frame[y][x][1],frame[y][x][0]]
        except:
            pixel = [0,0,0]
        return pixel

    # Populates a strip with rgb values
    def get_rgb_strip(self, frame, num_pixels):
        rgb_strip = [(self.get_rgb(frame, num_pixels, 0))]
        for i in range(1,num_pixels):
            rgb_strip.append((self.get_rgb(frame, num_pixels, i)))
        return rgb_strip
        
    # Takes input data and calculates led positions relative to starting point and saves to "strip"
    def set_strip(self,num_pixels, start_pos, angle, length):
        for i in range(1, (num_pixels)):
            y = ((length/num_pixels) * i) * math.sin(math.radians(angle))
            x = ((length/num_pixels) * i) * math.cos(math.radians(angle))
            self.strip.append((start_pos[0] + x, start_pos[1] + y))
            #print(x,y)
            
    # Draws led strips on the video window    
    def draw_strip(self,frame, start_pos, angle, length):
        x_end = int(length * math.cos(math.radians(angle))) + start_pos[0]
        y_end = int(length * math.sin(math.radians(angle))) + start_pos[1]
        #print(x_end, y_end, start_pos, angle, length)
        frame_drawn = cv2.line(frame, (start_pos[0], start_pos[1]), (x_end, y_end), (0,0,255),5)
        return frame_drawn


