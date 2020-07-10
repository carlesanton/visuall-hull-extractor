from sift import compute_sift_descriptor_of_image, compute_sift_matches
import os
import cv2
import random
from matplotlib import pyplot as plt
import numpy as np

def compute_fundamental_matrix():
    calibration_images_folder_path = os.path.join(os.getcwd(),'visuall_hull_extractor/calibration_images/v3labs')
    
    target_file = 'figures1.jpg'
    reference_file = 'figures2.jpg'

    target_image = cv2.imread(os.path.join(calibration_images_folder_path,target_file),0)
    reference_image = cv2.imread(os.path.join(calibration_images_folder_path,reference_file),0)
    
    sift = cv2.xfeatures2d.SIFT_create()
    reference_sift_points = compute_sift_descriptor_of_image(sift,reference_image)
    target_sift_points = compute_sift_descriptor_of_image(sift,target_image)

    matcher = cv2.BFMatcher()
    matches = compute_sift_matches(matcher,reference_sift_points['descriptors'],target_sift_points['descriptors'])

    reference_sample_points = []
    target_sample_points = []
    for match in matches:
        reference_sample_points.append(reference_sift_points['keypoints'][match.queryIdx].pt)
        target_sample_points.append(target_sift_points['keypoints'][match.trainIdx].pt)

    fundamental_matrix, inlier_mask = cv2.findFundamentalMat(np.float32(reference_sample_points),np.float32(target_sample_points), method=cv2.FM_RANSAC)


    # We select only inlier points
    reference_points = np.asarray(reference_sample_points, dtype=np.int32)[inlier_mask.ravel()==1]
    target_points =  np.asarray(target_sample_points, dtype=np.int32)[inlier_mask.ravel()==1]

    # Find epilines corresponding to points in right image (second image) and
    # drawing its lines on left image
    lines1 = cv2.computeCorrespondEpilines(target_points.reshape(-1,1,2), 2, fundamental_matrix)
    lines1 = lines1.reshape(-1,3)
    img5,img6 = drawlines(reference_image,target_image,lines1,reference_points,target_points)

    # Find epilines corresponding to points in left image (first image) and
    # drawing its lines on right image
    lines2 = cv2.computeCorrespondEpilines(reference_points.reshape(-1,1,2), 1,fundamental_matrix)
    lines2 = lines2.reshape(-1,3)
    img3,img4 = drawlines(target_image,reference_image,lines2,target_points,reference_points)

    plt.subplot(121),plt.imshow(img5)
    plt.subplot(122),plt.imshow(img3)
    plt.show()


    return fundamental_matrix, inlier_mask


def drawlines(img1,img2,lines,pts1,pts2):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r,c = img1.shape
    img1 = cv2.cvtColor(img1,cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2,cv2.COLOR_GRAY2BGR)
    for r,pt1,pt2 in zip(lines,pts1,pts2):
        color = tuple(np.random.randint(0,255,3).tolist())
        x0,y0 = map(int, [0, -r[2]/r[1] ])
        x1,y1 = map(int, [c, -(r[2]+r[0]*c)/r[1] ])
        img1 = cv2.line(img1, (x0,y0), (x1,y1), color,1)
        img1 = cv2.circle(img1,tuple(pt1),5,color,-1)
        img2 = cv2.circle(img2,tuple(pt2),5,color,-1)
    return img1,img2



if __name__ == "__main__":
    compute_fundamental_matrix()
