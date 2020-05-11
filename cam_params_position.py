import os
import cv2
import argparse

from sift import compute_sift_points_for_template_and_calibration_images, match_sift_points, save_all_keypoint_matches_images
from homography import compute_homography_for_all_calibration_images
from camera_utils import compute_internal_params, compute_external_params_for_all_images, plot_cameras

def load_images(calibration_images_folder_path):
    extensions = ['jpg', 'jpeg', 'png', 'tiff']
    calibration_images = []
    
    print("Reading images")
    for file in os.listdir(calibration_images_folder_path):
        file_name = file.split('.')[0]
        file_extension = file.split('.')[-1]
        if file.split('.')[-1] in extensions:
            image = cv2.imread(os.path.join(calibration_images_folder_path,file),0)
            if file_name == 'template_image':
                template_image = image
            elif 'calibration_image' in file_name:
                calibration_images.append(image)

    return template_image, calibration_images

 
def get_calibration_matrix_and_external_params(args):

    template_image, calibration_images = load_images(args.calibration_folder)

    template_points, calibration_points = compute_sift_points_for_template_and_calibration_images(template_image, calibration_images)

    matches = match_sift_points(template_points, calibration_points)
    
    homographies, inliers_masks = compute_homography_for_all_calibration_images(matches, template_points, calibration_points)

    save_all_keypoint_matches_images(template_image, calibration_images, template_points['keypoints'], calibration_points, matches, inliers_masks, homographies)

    camera_parameters = compute_internal_params(homographies)

    external_parameters_list = compute_external_params_for_all_images(camera_parameters, homographies)

    plot_cameras(external_parameters_list)
    


    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--show_images","-S", help='Show inliers projection images',action="store_true")
    parser.add_argument("--calibration_folder", "-f", default = os.path.join(os.getcwd(),'calibration_images'))

    args = parser.parse_args()
    get_calibration_matrix_and_external_params(args)


