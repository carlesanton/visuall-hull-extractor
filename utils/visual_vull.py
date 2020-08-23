from ctypes import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from Camera import Camera
import numpy as np
import sys
from typing import List
from pyrr import Vector3, Vector4
from PIL import Image

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

class VHullShader:


    # initialise opengl
    # from https://rdmilligan.wordpress.com/2016/08/27/opengl-shaders-using-python/
    def __init__(self, vhull_vertex):
    
        # load shaders code
        self.vhull_vertex_shader = open('./visuall_hull_extractor/shaders/vertex_shader_lite.glsl','r').read()
        self.vhull_fragment_shader = open('./visuall_hull_extractor/shaders/fragment_shader_lite.glsl','r').read()

        # create shader program
        self.program = self.compile_program(self.vhull_vertex_shader, self.vhull_fragment_shader)
        self.enable()
        
        # obtain uniforms and attributes locations
        self.a_vert = glGetAttribLocation(self.program, "vert")
        
        # Create VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Create VBO
        self.vertex_data = vhull_vertex.flatten()
        self.vertex_size = 2
        array_type = (GLfloat * len(self.vertex_data))
        self.vertex_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vertex_buffer)
        glBufferData(GL_ARRAY_BUFFER, ctypes.sizeof(ctypes.c_float) * len(self.vertex_data), array_type(*self.vertex_data), GL_STATIC_DRAW)
        glEnableVertexAttribArray(self.a_vert)
        glVertexAttribPointer(self.a_vert, self.vertex_size, GL_FLOAT, GL_FALSE, 0, None)
        
        # unbind buffers
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        '''###############
        self.u_model_matrix = glGetUniformLocation(self.program, 'model_matrix')
        self.u_proj_matrix_viewing_cam = glGetUniformLocation(self.program, 'projection_matrix_viewing_cam')
        self.u_view_matrix_viewing_cam = glGetUniformLocation(self.program, "view_matrix_viewing_cam")
        '''
        
        '''
        self.u_proj_matrix_model_cam = glGetUniformLocation(self.program, 'projection_matrix_model_cam')
        self.u_view_matrix_model_cam_1 = glGetUniformLocation(self.program, "view_matrix_model_cam_1")
        self.u_view_matrix_model_cam_2 = glGetUniformLocation(self.program, "view_matrix_model_cam_2")

        # Get image uniforms locations        
        self.u_model_cam_1_image = glGetUniformLocation(self.program, "model_cam_1_image")
        self.u_model_cam_2_image = glGetUniformLocation(self.program, "model_cam_2_image")

        # Bind the uniform samplers to texture units
        glUniform1i(self.u_model_cam_1_image, 0);
        glUniform1i(self.u_model_cam_2_image,  1);
        '''
    

        '''
        # load cube shilouette
        self.cube_shilouette_path = '/home/carles/repos/3d-environment/visuall_hull_extractor/calibration_images/square_mask.png'
        cube_shilouette_image = Image.open(self.cube_shilouette_path)
        cube_shilouette_data = np.array(list(cube_shilouette_image.getdata()), np.uint8)
        self.cube_shilouette_data_rgb = np.vstack((cube_shilouette_data, cube_shilouette_data, cube_shilouette_data))

        # set background texture
        self.textue_model_cam_1_image_handle = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textue_model_cam_1_image_handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, cube_shilouette_image.size[0], cube_shilouette_image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.cube_shilouette_data_rgb)
        
        self.textue_model_cam_2_image_handle = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.textue_model_cam_2_image_handle)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, cube_shilouette_image.size[0], cube_shilouette_image.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, self.cube_shilouette_data_rgb)
        '''
        
        self.disable()


    def render(self, viewing_camera: Camera, modeling_cameras: List[Camera]):   
        # get modeling projection matrix
        modeling_proj_matrix = modeling_cameras[0].get_projection_matrix()
        
        # get modeling projection matrix
        viewing_proj_matrix = viewing_camera.get_projection_matrix()
    
        # view matrix for each camera
        model_matrix = np.array([
            1.0, 0.0,  0.0, 0.0,
            0.0, 1.0,  0.0, 0.0,
            0.0, 0.0,  1.0, 0.0,
            0.0, 0.0, 0.0, 1.0], np.float32)
        
        # use shader program
        # set uniforms
        '''#####
        mvp = np.asarray(model_matrix).reshape((4,4)) * viewing_camera.get_view_matrix() * viewing_proj_matrix
        glUniformMatrix4fv(self.u_mvp, 1, GL_FALSE, mvp)
        glUniformMatrix4fv(self.u_model_matrix, 1, GL_FALSE, model_matrix)
        glUniformMatrix4fv(self.u_proj_matrix_viewing_cam, 1, GL_FALSE, viewing_proj_matrix)
        glUniformMatrix4fv(self.u_view_matrix_viewing_cam, 1, GL_FALSE, viewing_camera.get_view_matrix())
        '''
        
        
        '''    
        glUniformMatrix4fv(self.u_proj_matrix_model_cam, 1, GL_FALSE, modeling_proj_matrix)
        glUniformMatrix4fv(self.u_view_matrix_model_cam_1, 1, GL_FALSE, modeling_cameras[0].get_view_matrix())
        glUniformMatrix4fv(self.u_view_matrix_model_cam_2, 1, GL_FALSE, modeling_cameras[1].get_view_matrix())
        '''    
        
        # enable attribute arrays
        # set vertex buffers
        self.enable()
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, int(len(self.vertex_data)/self.vertex_size))
        glBindVertexArray(0)
        self.disable()
        
        
        '''    
        # bind modeling camera images
        glActiveTexture(GL_TEXTURE0 + 0); # Texture unit 0
        glBindTexture(GL_TEXTURE_2D, self.textue_model_cam_1_image_handle)

        glActiveTexture(GL_TEXTURE0 + 1); # Texture unit 1
        glBindTexture(GL_TEXTURE_2D, self.textue_model_cam_2_image_handle)
        '''   

    def short_render(self, viewing_camera: Camera, modeling_cameras: List[Camera]):
        self.enable()
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, int(len(self.vertex_data)/self.vertex_size))
        glBindVertexArray(0)
        self.disable()
        

    # from PySpace
    def compile_shader(self, source, shader_type):
        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        status = c_int()
        glGetShaderiv(shader, GL_COMPILE_STATUS, byref(status))
        if not status.value:
            self.print_log(shader)
            glDeleteShader(shader)
            raise ValueError('Shader compilation failed')
        return shader

    # from PySpace
    def compile_program(self, vertex_source, fragment_source):
        vertex_shader = None
        fragment_shader = None
        program = glCreateProgram()

        if vertex_source:
            print("Compiling Vertex Shader...")
            vertex_shader = self.compile_shader(vertex_source, GL_VERTEX_SHADER)
            glAttachShader(program, vertex_shader)
        if fragment_source:
            print("Compiling Fragment Shader...")
            fragment_shader = self.compile_shader(fragment_source, GL_FRAGMENT_SHADER)
            glAttachShader(program, fragment_shader)

        glLinkProgram(program)
        result = glGetProgramiv(program, GL_LINK_STATUS)
        info_log_len = glGetProgramiv(program, GL_INFO_LOG_LENGTH)
        if info_log_len:
            print("Error linking program...")
            sys.exit(11)


        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        return program

    # from PySpace
    def print_log(self, shader):
        length = c_int()
        glGetShaderiv(shader, GL_INFO_LOG_LENGTH, byref(length))

        if length.value > 0:
            log = create_string_buffer(length.value)
            print(glGetShaderInfoLog(shader))

    def enable(self):
        glUseProgram(self.program)
        assert(glGetError() == GL_NO_ERROR)

        self.last_slot = 0
    
    def disable(self):
        glUseProgram(0)
        glActiveTexture(GL_TEXTURE0)
        assert(glGetError() == GL_NO_ERROR)