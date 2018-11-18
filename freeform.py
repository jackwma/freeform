import cv2
from math import sqrt
import matplotlib
import matplotlib.pyplot as plt 
import numpy as np 
from backproj import mask, getHistogram
from contours import getContours, handleContours

centers = []
pixels = []
beta = .3

FRAME_HEIGHT = 600
FRAME_WIDTH = 800

def getContourCenter(contours, frame=None, draw_center=False):
	if len(contours) > 0:
		center = (0,0)
		for cnt in contours:
			(x, y, w, h) = cv2.boundingRect(cnt)
			center = (x + w // 2, y + h // 2)
			if draw_center:
				if x == None:
					cv2.circle(frame, centers[-1], 2, (0, 255, 0), 3)
				else:
					if len(pixels) == 0:
						pixels.append(center)
					pixel_x = int(beta * pixels[-1][0] + (1 - beta) * center[0])
					pixel_y = int(beta * pixels[-1][1] + (1 - beta) * center[1])
					pixels.append((pixel_x, pixel_y))
					cv2.circle(frame, pixels[-1], 3, (0, 0, 0), 3)
		return center


def getLength(p1, p2):
	return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def drawCenters(pixels, frame):
	size = len(pixels)
	for i in range(size):
		if i > 0:
			p = pixels[i]
			p_last = pixels[i - 1]
			if p_last != None and p != None and getLength(p_last, p) < 200:
					cv2.line(frame, p_last, p, (0, 255, 0), 4)
	
def handleCenters(centers):
	if len(pixels) > 400:
		del pixels[0]	
	if len(centers) > 400:
		del centers[0]

def startVideoFeed(cam_index, hist=None):

	# Args:
		# cam_index (int): 0 for webcam; 1 for USB camera
		# hist (numpy array): histogram for masking
	cap = cv2.VideoCapture(cam_index)
	while(True):
		_, frame = cap.read()
		thresh_frame = mask(roi_hist, frame)
		contours = getContours(thresh_frame)
		contours = handleContours(contours)
		canvas = np.ones(frame.shape) * 255
		centers.append(getContourCenter(contours, canvas, draw_center=True))
		drawCenters(pixels, canvas)
		#drawCenters(pixels, frame)
		canvas = np.flip(canvas, 1)
		canvas_resized = cv2.resize(canvas, (FRAME_WIDTH, FRAME_HEIGHT))
		cv2.imshow('canvas', canvas_resized)
		#cv2.imshow('frame', frame_resized)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	cap.release()
	cv2.destroyAllWindows()


roi_img = cv2.imread('./images/roi.jpg', 3)
roi_hist = getHistogram(roi_img)



startVideoFeed(0)
