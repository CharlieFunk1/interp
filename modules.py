import cv2
import numpy as np
import math

class Rgbstrip:
    #initialize the object with starting position in array "strip" and run set_strip to add coordinates
    def __init__(self, num_pixels, start_pos, angle, length):
        self.strip = [(start_pos[0], start_pos[1])]
        self.set_strip(num_pixels, start_pos, angle, length)

    # Gets the RGB values from led (i) on the strip.  Returns (R,G,B)
    def get_rgb(self, frame, num_pixels, i):
        x = int(self.strip[i][0])  #int(((frame.shape[1]-1) / num_pixels) * i)
        y = int(self.strip[i][1])  #int((strip_hposition * .01) * frame.shape[0])
        pixelB = frame[y][x][0]
        pixelG = frame[y][x][1]
        pixelR = frame[y][x][2]
        pixel = [pixelR,pixelG,pixelB]
        return pixel

    # Takes input data and calculates led positions relative to starting point and saves to "strip"
    def set_strip(self,num_pixels, start_pos, angle, length):
        for i in range(1, (num_pixels)):
            y = ((length/num_pixels) * i) * math.sin(angle)
            x = ((length/num_pixels) * i) * math.cos(angle)
            self.strip.append((start_pos[0] + x, start_pos[1] + y))
            #print(x,y)
            
    # Draws led strips on the video window    
    def draw_strip(self,frame, start_pos, angle, length):
        frame_drawn = cv2.line(frame, (start_pos[0], start_pos[1]), (int(length * math.cos(angle) + start_pos[0]), int(length*math.sin(angle) + start_pos[1])), (0,0,255),5)
        return frame_drawn


