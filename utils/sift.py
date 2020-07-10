import cv2
import numpy as np
import os


def compute_sift_descriptor_of_image(sift,img):
    kp, des = sift.detectAndCompute(img,None)
    keypoints = {}
    keypoints['keypoints'] = kp
    keypoints['descriptors'] = des
    return keypoints

def compute_sift_points_for_template_and_calibration_images(template_image, calibration_images):
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    # template descriptors
    print("Computing sift points for template image")
    template_points = compute_sift_descriptor_of_image(sift,template_image)
    # calibraation descriptors
    print("Computing sift points for calibration images")
    calibration_points=[compute_sift_descriptor_of_image(sift,image) for image in calibration_images]

    return template_points, calibration_points

def compute_sift_matches(matcher,des1,des2):
    
    matches = matcher.knnMatch(des1,des2, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
    return good

def match_sift_points(template_points, calibration_points):
    # create BFMatcher with default params
    matcher = cv2.BFMatcher()
    # Compute matches
    print("Computing matches")
    matches=[compute_sift_matches(matcher,template_points['descriptors'],cal_points['descriptors']) for cal_points in calibration_points]

    return matches

def get_keypoint_matches_image(template_image, calibration_image, template_keypoints, calibration_keypoints, matches, inliers_mask, image_homography, save_folder):
    # To project template borders into transformed image
    h,w = template_image.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    template_corners = cv2.perspectiveTransform(pts,image_homography)
    calibration_image_with_template_borders = cv2.polylines(calibration_image,[np.int32(template_corners)],True,255,3, cv2.LINE_AA)


    draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                    singlePointColor = None,
                    matchesMask = inliers_mask, # draw only inliers
                    flags = 2)
    final_image = cv2.drawMatches(template_image,template_keypoints,calibration_image_with_template_borders,calibration_keypoints,matches,None,**draw_params)
    
    return final_image
    

def save_all_keypoint_matches_images(template_image, calibration_images, template_points, calibration_points, matches_list, inliers_masks, image_homographies, save_folder = 'sift_matches'):
    for calibration_image, calibration_points_of_image, matches, image_homography, inlier_mask in zip(calibration_images, calibration_points, matches_list, image_homographies, inliers_masks):
        matches_image = get_keypoint_matches_image(template_image, calibration_image, template_points, calibration_points_of_image['keypoints'], matches, inlier_mask, image_homography, save_folder = save_folder)

        if not os.path.isdir(save_folder):
            os.makedirs(save_folder)
        
        num_files_in_save_folder = len(list(os.listdir(save_folder)))

        cv2.imwrite(os.path.join(save_folder,f'matches_image_{num_files_in_save_folder}.png'), matches_image)