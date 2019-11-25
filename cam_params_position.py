import numpy as np
import os
import cv2
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse



#Compute camera internal parameters and the homographies between images so it can then plot the position of the cameras relative to the patter image


def compute_sift_descriptor(sift,img):
    kp, des = sift.detectAndCompute(img,None)
    return (kp, des)

def compute_sift_matches(bf,des1,des2):
    
    matches = bf.knnMatch(des1,des2, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)
    return good

def compute_homography(min_matches, matches, template_points, calibration_points, template_image, calibration_image, n, N, show_images):
    '''
    INPUTS

    min_matches = minimim number of matches to compute homography
    matches = index queryIdx tells which template points matches with the trainIdx image point
    template_points = points of template image where
    calibration_points = points of template calibration where
    template_image = template image used to get the descriptors
    calibration_image = calibration image used to get the calibration descriptors

    OUTPUTS

    M = homography that relates template and calibration image
    matchesMask = mask to know which of the matches are inliers and therefore true matches

    '''
    
    if len(matches)>min_matches:

        src_pts = np.float32([ template_points[m.queryIdx].pt for m in matches]).reshape(-1,1,2)
        dst_pts = np.float32([ calibration_points[0][m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

        print("Computing homography for image " + str(n+1) + " of " + str(N))
        M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
        matchesMask = mask.ravel().tolist()



        # To project template borders into transformed image
        h,w = template_image.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        template_corners = cv2.perspectiveTransform(pts,M)
        final_calibration_image = cv2.polylines(calibration_image,[np.int32(template_corners)],True,255,3, cv2.LINE_AA)
    else:
        print ("Not enough matches are found - " + str(len(matches)) + '/'+  str(min_matches))
        M = None
        matchesMask = None
    
    if show_images:
        draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                       singlePointColor = None,
                       matchesMask = matchesMask, # draw only inliers
                       flags = 2)
        final_image = cv2.drawMatches(template_image,template_points,final_calibration_image,calibration_points[0],matches,None,**draw_params)
        plt.imshow(final_image, 'gray')
        plt.show()


    return (M, matchesMask) 

def compute_internal_params(all_homographies):
    # Compute linear system of equations to compute IAC
    A = np.zeros((2 * len(all_homographies), 6),dtype=float)
    for i in range(len(all_homographies)):
        h = all_homographies[i]
        #v12
        A[2*i,:]=np.array([h[0,0] * h[0,1], 
                    h[0,0] * h[1,1] + h[1,0] * h[0,1], 
                    h[0,0] * h[2,1] + h[2,0] * h[0,1], 
                    h[1,0] * h[1,1], 
                    h[1,0] * h[2,1] + h[2,0] * h[1,1], 
                    h[2,0] * h[2,1]])
        #v11-v22
        A[2*i+1,:]=np.array([h[0,0] * h[0,0], 
                    h[0,0] * h[1,0] + h[1,0] * h[0,0], 
                    h[0,0] * h[2,0] + h[2,0] * h[0,0], 
                    h[1,0] * h[1,0], 
                    h[1,0] * h[2,0] + h[2,0] * h[1,0], 
                    h[2,0] * h[2,0]]) -  np.array([h[0,1] * h[0,1], 
                    h[0,1] * h[1,1] + h[1,1] * h[0,1],
                    h[0,1] * h[2,1] + h[2,1] * h[0,1], 
                    h[1,1] * h[1,1], 
                    h[1,1] * h[2,1] + h[2,1] * h[1,1], 
                    h[2,1] * h[2,1]])

    u, s, vh = np.linalg.svd(A, full_matrices = True)
    omega = vh.transpose()[:,-1]

    w =np.array([ [omega[0], omega[1], omega[2] ], 
                  [omega[1], omega[3], omega[4] ],   
                  [omega[2], omega[4], omega[5] ] ])
    # Get calibration maatrix by Cholesky decomposition
    K = np.linalg.cholesky(w)
    K = K/K[2,2]

    return K

def compute_external_params(K,h):

    r1 = np.linalg.inv(K).dot(h[:,0])
    r2 = np.linalg.inv(K).dot(h[:,1])
    t = np.linalg.inv(K).dot(h[:,2])

    # Solve the scale ambiguity by forcing r1 and r2 to be unit vectors.
    s = np.sqrt(np.linalg.norm(r1) * np.linalg.norm(r2)) * np.sign(t[2])

    r1 = r1 / s
    r2 = r2 / s
    t = t / s
    R =np.array([r1,r2,np.cross(r1,r2)]).transpose()


    # Ensure R is a rotation matrix
    U, S, V = np.linalg.svd(R, full_matrices = True)
    R = U * np.identity(3) * V.transpose()
    


    # Copute final camera projection matrix
    rrr=np.concatenate((R.transpose(), np.array([t])),axis=0).transpose()

    P = K.dot(rrr)


    return (R, t, P)

def plot_cameras(external_params):
    camera_centers_xs = [ext[1][0] for ext in external_params]
    camera_centers_ys = [ext[1][1] for ext in external_params]
    camera_centers_zs = [ext[1][2] for ext in external_params]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')


    ax.scatter(0,0,0,c='r', marker='o')
    ax.scatter(camera_centers_xs,camera_centers_ys,camera_centers_zs,c='b', marker='^')

    plt.show()

def get_calibration_matrix_and_external_params(args):

    folder_path = 'C:/Users/Carles/Documents/Code/visualhull/get image/calibrate'
    MIN_MATCH_COUNT = 10
    print("Reading images")
    template_image = cv2.imread(os.path.join(folder_path,'template.jpg'),0)
    calibration_images=[cv2.imread(os.path.join(folder_path,'takes',image),0) for image in os.listdir(os.path.join(folder_path,'takes'))]


    # Initiate SIFT detector and BFMatcher with default params
    sift = cv2.xfeatures2d.SIFT_create()
    bf = cv2.BFMatcher()

    # find the keypoints and descriptors with SIFT
    # calibraation descriptors
    print("Finding keypoints")
    calibration_descriptors=[compute_sift_descriptor(sift,image) for image in calibration_images]
    # template descriptors
    template_descriptors = compute_sift_descriptor(sift,template_image)


    # Compute matches
    print("Computing matches")
    matches=[compute_sift_matches(bf,template_descriptors[1],des[1]) for des in calibration_descriptors]

    #compute homographies and inliers
    homog_and_masks = [compute_homography(MIN_MATCH_COUNT, matches[presp], template_descriptors[0], calibration_descriptors[presp],calibration_images[presp], template_image, presp, len(calibration_descriptors), args.show_images) for presp in range(len(calibration_descriptors))]
    
    # store homographies and matches inliers masks separately
    homographies = [f[0] for f in homog_and_masks]
    masks = [f[1] for f in homog_and_masks]

    K = compute_internal_params(homographies)
    print(K)
    
    external_params = []
    [external_params.append(compute_external_params(K,h)) for h in homographies]
    
    plot_cameras(external_params)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--show_images","-S", help='Show inliers projection images',action="store_true")
    
    args = parser.parse_args()
    get_calibration_matrix_and_external_params(args)


