import cv2
import numpy as np
purple_l = np.array([130,80,50])
purple_u = np.array([160,255,255])
red1_l = np.array([0,120,70])
red1_u = np.array([10,255,255])
red2_l = np.array([170,120,70])
red2_u = np.array([180,255,255])
blue_l = np.array([100,120,50])
blue_u = np.array([130,255,255])
min = 1000
roiy,roix = 130,180
roi_height,roi_width = 180,250
def statement(frame):
    rotatedframe = cv2.rotate(frame,cv2.ROTATE_180)
    roi = rotatedframe[130:310,180:430]
    hsv = cv2.cvtColor(roi,cv2.COLOR_BGR2HSV)
    ball_r1 = cv2.inRange(hsv,red1_l,red1_u)
    ball_r2 = cv2.inRange(hsv,red2_l,red2_u)
    ball_r = ball_r1 + ball_r2
    r_pixel = cv2.countNonZero(ball_r)
    ball_p = cv2.inRange(hsv,purple_l,purple_u)
    p_pixel = cv2.countNonZero(ball_p)
    ball_b = cv2.inRange(hsv,blue_l,blue_u)
    b_pixel = cv2.countNonZero(ball_b)
    color = {'red':r_pixel,'purple':p_pixel,'blue':b_pixel}
    dominant_color = max(color,key = color.get)
    count = color[dominant_color]
    if count < min:
        return"NO ball"
    else:
        return dominant_color
    # for i,j in color.items():
    #     if j < min:
    #         return"No ball"
    #     else:
    #         return i
def process(project):
    cam = cv2.VideoCapture(project)
    cnt = 0
    while cam.isOpened():
        ret,frame = cam.read()
        frame = cv2.rotate(frame,cv2.ROTATE_180)
        if not ret:
            break
        condition = statement(frame)
        cv2.rectangle(frame,(180,130),(430,310),(0,255,0),2)
        cv2.putText(frame,condition,(30,50),cv2.FONT_HERSHEY_SIMPLEX,1.2,(255,255,255),3)
        cv2.imshow('video',frame)
        cv2.waitKey(25)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    cam.release()
process('res/output.avi')
process('res/output1.avi')
