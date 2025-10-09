import cv2
import numpy as np
import json
class Balldector:
    roi_x = None
    roi_y = None
    roi_w = None
    roi_h = None
    red1_low = None
    red1_up = None
    red2_low = None
    red2_up = None
    blue_low = None
    blue_up = None
    purple_low = None
    purple_up = None
    min_pixel_threshold = 500
    display_debug_info = True
    color_ranges = None
    def __init__(self,profile):
        self.profile = profile
        self.load_config()
    def load_config(self):
        with open(self.profile,'r',encoding='utf-8') as file:
            config = json.load(file)
        roi_config = config.get('roi',{})
        self.roi_x = roi_config.get('x',100)
        self.roi_y = roi_config.get('y',100)
        self.roi_height = roi_config.get('height',200)
        self.roi_width = roi_config.get('width',200)
        self.color_range = config.get('color_range',{})
        self.red1_l = np.array(self.color_range.get('red1',[])[0])
        self.red1_u = np.array(self.color_range.get('red1',[])[1])
        self.red2_l = np.array(self.color_range.get('red2',[])[0])
        self.red2_u = np.array(self.color_range.get('red2',[])[1])
        self.blue_l = np.array(self.color_range.get('blue',[])[0])
        self.blue_u = np.array(self.color_range.get('blue',[])[1])
        self.purple_l = np.array(self.color_range.get('purple',[])[0])
        self.purple_u = np.array(self.color_range.get('purple',[])[1])
        min = 1000
    def get_ball(self,frame):
        rotated_frame = cv2.rotate(frame,cv2.ROTATE_180)
        roi = rotated_frame[130:310,180:430]
        hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
        red_mask1 = cv2.inRange(hsv,self.red1_l,self.red1_u)
        red_mask2 = cv2.inRange(hsv,self.red2_l,self.red2_u)
        red_mask = red_mask1 + red_mask2
        blue_mask = cv2.inRange(hsv,self.blue_l,self.blue_u)
        purple_mask = cv2.inRange(hsv,self.purple_l,self.purple_u)
        red_pixel = cv2.countNonZero(red_mask)
        blue_pixel = cv2.countNonZero(blue_mask)
        purple_pixel = cv2.countNonZero(purple_mask)
        color = {'red':red_pixel,'blue':blue_pixel,'purple':purple_pixel}
        dominant_color = max(color,key = color.get)
        color_count = color[dominant_color]
        if color_count < min:
            return 'No ball'
        else:
            return dominant_color
    def process(self,project):
        self.load_config()
        cam = cv2.VideoCapture(project)
        cnt = 0
        while cam.isOpened():
            ret,frame = cam.read()
            frame = cv2.rotate(frame,cv2.ROTATE_180)
            condition = self.get_ball(frame)
            cv2.rectangle(frame,(180,130),(430,310),(0,255,0),2)
            cv2.putText(frame,condition,(30,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),3)
            cv2.imshow('video',frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        cam.release()
ball = Balldector('config.json')
ball.process('res/output.avi')
ball.process('res/output1.avi')