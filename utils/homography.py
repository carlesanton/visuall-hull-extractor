import numpy as np
import os
import cv2

def compute_homography_for_all_calibration_images(matches, template_points, calibration_points):
    #compute homographies and inliers
    count = 1
    homog_and_masks = []
    for match, cal_points in zip(matches, calibration_points):
        print(f'Computing homography for image {count}')
        homog_and_masks.append(compute_homography(match,
                        template_points['keypoints'],
                        cal_points['keypoints']))
        count+=1

    # store homographies and matches inliers masks separately
    homographies = [f[0] for f in homog_and_masks]
    inliers_masks = [f[1] for f in homog_and_masks]
    return homographies, inliers_masks

def compute_homography(matches, template_points, calibration_points, min_matches = 10):
    '''
    INPUTS

    matches = index queryIdx tells which template points matches with the trainIdx image point
    template_points = points of template image where
    calibration_points = points of template calibration where

    min_matches = minimim number of matches to compute homography

    OUTPUTS

    M = homography that relates template and calibration image
    matchesMask = mask to know which of the matches are inliers and therefore true matches
    '''
    
    if len(matches)>min_matches:
        src_pts = np.float32([ template_points[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
        dst_pts = np.float32([ calibration_points[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        
        H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()

    else:
        print ("Not enough matches are found - " + str(len(matches)) + '/'+  str(min_matches))
        H = None
        matchesMask = None
    
        H = None
    return (H, matchesMask) 