import cv2
import numpy as np

width = 640
height = 480
middle_point = (int(height/2),int(width/2))
sq_prop = 0.2
sq_size = int(width*sq_prop)
sq_half_size = int(sq_size/2)
im  = np.zeros((height, width))
im[middle_point[0] - sq_half_size: middle_point[0] + sq_half_size,
   middle_point[1] - sq_half_size: middle_point[1] + sq_half_size] = 255.

cv2.imwrite('/home/carles/repos/3d-environment/visuall_hull_extractor/calibration_images/square_mask.png', im)