from ctypes import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from Camera import Camera
import numpy as np
import sys
from typing import List
from pyrr import Vector3, Vector4
from PIL import Image
from visuall_hull_extractor.utils.Object import TextureObject
from Shaders import TextureShader

sys.path.append('..')


class Voxel:

    def __init__(self, x_cord: float, y_cord: float, z_cord: float, size: float):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.z_cord = z_cord
        self.position = np.array([x_cord, y_cord, z_cord])
        self.size = size

        self.is_inside_model = True

    def render(self) -> None:
        if self.is_inside_model:
            glColor3f(0.0, 0.0, 1.0)

            # vertical lines
            glVertex3fv((self.x_cord + self.size/2.,
                         self.y_cord + self.size/2.,
                         self.z_cord + self.size/2.))


class VoxelGrid:

    def __init__(self, lin_space):
        try:
            self.voxel_size = lin_space[1]-lin_space[0]
        except:
            raise 'lin_space too small'

        self.voxels = []
        self.initialise_voxels(lin_space)

    def initialise_voxels(self, lin_space):
        for x in lin_space:
            for y in lin_space:
                for z in lin_space:
                    self.voxels.append(
                        Voxel(x_cord=x, y_cord=y + max(lin_space), z_cord=z, size=self.voxel_size))

    def render(self):
        glBegin(GL_LINES)
        for voxel in self.voxels:
            voxel.render()
        glEnd()
        return None

    def carve_space(self, cameras: List[Camera]):
        glBegin(GL_LINES)
        for voxel in self.voxels:
            count = 0
            for camera in cameras:
                # for each check if voxel is inside its silhouette
                voxel_image_position = camera.project_3d_point_into_image_plane(
                    Vector3(voxel.position))
                if camera.check_point_in_silhouette(image_point=voxel_image_position):
                    voxel.is_inside_model = True
                    continue
                else:
                    voxel.is_inside_model = False
                    # don't check for more cameras since it is outside
                    break
            voxel.render()
        glEnd()

    def get_voxel_centers_as_np_array(self):
        voxel_centers = np.empty(shape = (len(self.voxels), 3), dtype = np.float32)
        for index, voxel in enumerate(self.voxels):
            voxel_centers[index, :] = voxel.position

        return voxel_centers

class VHullTextured(TextureObject):
    def __init__(
        self, 
        vhull_vertex,
        modeling_cameras = None,
        shader: TextureShader = None, 
        rendering_primitive = GL_TRIANGLE_STRIP,
    ):
        self.cube_shilouette_path = '/home/carles/repos/3d-environment/visuall_hull_extractor/calibration_images/v3labs/figures1.jpg'
        self.cube_shilouette_path = '/home/carles/repos/3d-environment/visuall_hull_extractor/calibration_images/square_mask.png'
        self.cube_shilouette_image = Image.open(self.cube_shilouette_path)
        self.modeling_cameras = modeling_cameras
        texture_images = [
            self.cube_shilouette_image,
            self.cube_shilouette_image,
        ]
        super().__init__(
            vhull_vertex, 
            texture_images, 
            shader, 
            rendering_primitive,
        )
        self.add_visual_hull_attributes_to_shader_()

    def add_visual_hull_attributes_to_shader(self):
        self.shader.enable()
        glBindVertexArray(self.vao)
        glPointSize(5.0)

        self.u_view_matrix_model_cam_1 = glGetUniformLocation(self.shader.program, "view_matrix_model_cam_1")
        self.u_view_matrix_model_cam_2 = glGetUniformLocation(self.shader.program, "view_matrix_model_cam_2")
        glUniformMatrix4fv(self.u_view_matrix_model_cam_1, 1, GL_FALSE, self.modeling_cameras[0].get_view_matrix())
        glUniformMatrix4fv(self.u_view_matrix_model_cam_2, 1, GL_FALSE, self.modeling_cameras[1].get_view_matrix())

        # Modeling focal lenghts
        self.u_focal_length_modeling_cam_1 = glGetUniformLocation(self.shader.program, "modeling_cam_1_focal_length")
        self.u_focal_length_modeling_cam_2 = glGetUniformLocation(self.shader.program, "modeling_cam_2_focal_length")
        glUniform2f(self.u_focal_length_modeling_cam_1, self.modeling_cameras[0].focal_length[0], self.modeling_cameras[0].focal_length[1])
        glUniform2f(self.u_focal_length_modeling_cam_2, self.modeling_cameras[1].focal_length[1], self.modeling_cameras[1].focal_length[1])

        # Modeling Image Centers
        self.u_image_center_modeling_cam_1 = glGetUniformLocation(self.shader.program, "modeling_cam_1_image_center")
        self.u_image_center_modeling_cam_2 = glGetUniformLocation(self.shader.program, "modeling_cam_2_image_center")
        glUniform2f(self.u_image_center_modeling_cam_1, self.modeling_cameras[0].principal_point[0], self.modeling_cameras[0].principal_point[1])
        glUniform2f(self.u_image_center_modeling_cam_2, self.modeling_cameras[1].principal_point[0], self.modeling_cameras[1].principal_point[1])
        
        glBindVertexArray(0)
        self.shader.disable()

    def add_visual_hull_attributes_to_shader_(self):
        self.shader.enable()
        glBindVertexArray(self.vao)
        glPointSize(5.0)

        self.u_view_matrix_model_cam_1 = glGetUniformLocation(self.shader.program, "view_matrix_model_cam_1")
        glUniformMatrix4fv(self.u_view_matrix_model_cam_1, 1, GL_FALSE, self.modeling_cameras[0].get_view_matrix())
        self.u_view_matrix_model_cam_2 = glGetUniformLocation(self.shader.program, "view_matrix_model_cam_2")
        glUniformMatrix4fv(self.u_view_matrix_model_cam_2, 1, GL_FALSE, self.modeling_cameras[1].get_view_matrix())
        
        self.u_view_matrix_model_cam_1 = glGetUniformLocation(self.shader.program, "projection_matrix_model_cam_1")
        glUniformMatrix4fv(self.u_view_matrix_model_cam_1, 1, GL_FALSE, self.modeling_cameras[0].get_projection_matrix())
        self.u_view_matrix_model_cam_2 = glGetUniformLocation(self.shader.program, "projection_matrix_model_cam_2")
        glUniformMatrix4fv(self.u_view_matrix_model_cam_2, 1, GL_FALSE, self.modeling_cameras[1].get_projection_matrix())

        glBindVertexArray(0)
        self.shader.disable()
