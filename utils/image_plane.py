from OpenGL.GL import *

from visuall_hull_extractor.utils.Object import TextureObject


class ImagePlane(TextureObject):
    def __init__(
        self, 
        vertices, 
        texture_images, 
        shader = None, 
        rendering_primitive = GL_LINES,
    ):
        super().__init__(
            vertices, 
            texture_images, 
            shader, 
            rendering_primitive,
        )