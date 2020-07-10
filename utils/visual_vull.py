import numpy as np
import sys
from typing import List

sys.path.append('..')
from Camera import Camera


'''
def point_inside_silhouette(silhouette_image: np.array, image_point: np.array): -> bool
'''



class Voxel:
    
    def  __init__(self, x_cord: float, y_cord: float, z_cord: float):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.z_cord = z_cord
        self.position = np.array([x_cord, y_cord, z_cord])

        self.is_inside_model = True


def main():

    model_size = 5

    voxels = generate_boxel_space(model_size)


    for voxel in voxels:
        for camera in cameras:
            # for each check if voxel is inside its silhouette
            # TODO: put into a function 
            voxel_image_position = project_point_into_camera_plane(camera, voxel.position)
            if point_inside_silhouette(shilouette = camera, image_point = voxel_image_position):
                continue
            else:
                voxel.is_inside_model = False
                # don't check for more cameras since it is outside
                break

def generate_boxel_space(model_size: int): -> List[Voxels]
    voxels = []
    for x in range(model_size):
        for y in range(model_size):
            for z in range(model_size):
                voxels.append(Voxel(x_cord = x, y_cord = y, z_cord = z))

    return voxels