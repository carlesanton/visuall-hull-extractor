import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from PIL import Image

class Object:

    def __init__(self, vertices, colors, shader = None, rendering_primitive = GL_LINES):
        self.vertex_size  = len(vertices[0])
        self.vertices_data = vertices.flatten()
        self.colors_data = colors.flatten()
        self.shader = shader
        self.rendering_primitive = rendering_primitive
        if self.shader:
            self.init_gl_vertex_and_color_buffers()

    def init_gl_vertex_and_color_buffers(self):        
        self.vao = self.shader.init_gl_vertex_and_color_buffers_into_vao(
                                    self.vertices_data, 
                                    self.colors_data, 
                                    self.vertex_size,
                                )

    def render(self):
        self.shader.enable()
        # render object
        glBindVertexArray(self.vao)
        glDrawArrays(self.rendering_primitive, 0, int(len(self.vertices_data)/self.vertex_size))
        glBindVertexArray(0)
        self.shader.disable()

class TextureObject():
    def __init__(self, vertices, texture_images, shader = None, rendering_primitive = GL_LINES):
        self.vertex_size  = len(vertices[0])
        self.vertices_data = vertices.flatten()
        self.shader = shader
        self.rendering_primitive = rendering_primitive
        
        try:
            self.create_uv_vertices(vertices)
        except:
            self.uv_coordinates = None
            
        self.texture_images_list = [
            self.image_to_np_3d_array(texture_image)
            for texture_image in texture_images
        ]
        self.texture_images_bytes_list = [
            self.image_to_bytes(texture_image)
            for texture_image in self.texture_images_list
        ]
        
        if self.shader:
            self.init_gl_buffers()

    def image_to_np_3d_array(self, texture_image):
        texture_image = np.array(texture_image, dtype=np.uint8)
        if texture_image.ndim == 2:
            texture_image = self.turn_2d_image_into_3d(texture_image)

        return texture_image

    def image_to_bytes(self, texture_image):
        return Image.fromarray(texture_image).convert("RGBA").tobytes()

    def init_gl_buffers(self):        
        self.vao = self.shader.init_gl_buffers(
                        self.vertices_data, 
                        self.uv_coordinates, 
                        self.texture_images_bytes_list, 
                        self.vertex_size, 
                        self.texture_images_list[0].shape
                    )

    def create_uv_vertices(self, vertices):
        v = vertices[:,0:2]
        self.bottom_left_corner = np.sum(v == min(v[:,1]), axis = 1, dtype = bool) * np.sum(v == min(v[:,0]), axis = 1, dtype = bool)
        self.top_left_corner = np.sum(v == max(v[:,1]), axis = 1, dtype = bool) * np.sum(v == min(v[:,0]), axis = 1, dtype = bool)
        self.top_right_corner = np.sum(v == max(v[:,1]), axis = 1, dtype = bool) * np.sum(v == max(v[:,0]), axis = 1, dtype = bool)
        self.bottom_right_corner = np.sum(v == min(v[:,1]), axis = 1, dtype = bool) * np.sum(v == max(v[:,0]), axis = 1, dtype = bool)
        
        uv_coordinates = np.empty([4,2],dtype=np.float32)
        uv_coordinates[self.bottom_left_corner, :] = [1.,1.]
        uv_coordinates[self.top_left_corner, :] = [1.,0.]
        uv_coordinates[self.top_right_corner, :] = [0.,0.]
        uv_coordinates[self.bottom_right_corner, :] = [0.,1.]

        self.uv_coordinates = uv_coordinates.flatten()
    
    def render(self):
        self.shader.enable()
        # render object
        glBindTexture(GL_TEXTURE_2D_ARRAY, self.shader.texture_image_buffer)
        glBindVertexArray(self.vao)
        glDrawArrays(self.rendering_primitive, 0, int(len(self.vertices_data)/self.vertex_size))
        glBindVertexArray(0)
        self.shader.disable()

    def update_texture_image(self, new_texture_image, image_index):
        texture_image = self.image_to_np_3d_array(new_texture_image)
        texture_image_bytes = self.image_to_bytes(texture_image)
        try:
            self.texture_images_list[image_index] = texture_image
            self.texture_images_bytes_list[image_index] = texture_image_bytes
        except IndexError as err:
            self.texture_images_list.append(texture_image)
            self.texture_images_bytes_list.append(texture_image_bytes)
        
        self.shader.update_texture_image(texture_image_bytes, image_index, texture_image.shape)

    @staticmethod
    def turn_2d_image_into_3d(image):
        return np.stack([image, image, image], axis = 2)


class Scene:

    def __init__(self):
        self.object_dict = {}

    def add_object(self, object_name, obj):
        self.object_dict[object_name] = obj

    def render(self):
        for _obj_name, obj in self.object_dict.items():
            obj.render()