from pyrr import Vector3, matrix44, Matrix44, vector, vector3, matrix33
from math import sin, cos, radians
import numpy as np
from OpenGL.GLU import *


#camera class to handle all movements and rotations


class Camera:
    def __init__(self, position, target):
        self.camera_pos = Vector3(position)
        self.target = Vector3(target)
        self.camera_front = Vector3(vector3.normalize(self.camera_pos - self.target))
        self.up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3(vector3.normalize(vector3.cross( self.up,self.camera_front)))
        self.camera_up = Vector3(vector3.cross(self.camera_right,self.camera_front))
        self.speed = 0.15
        self.rot_step = 0.025
        self.update_camera_vectors()

    def get_view_matrix(self):
        return self.look_at(self.camera_pos, self.target, self.camera_up)
    
    def cam_lookat(self):        
        glu_lookat =  gluLookAt(self.camera_pos.x,  self.camera_pos.y,  self.camera_pos.z,  self.target.x,  self.target.y,  self.target.z,  self.camera_up.x,  self.camera_up.y,  self.camera_up.z)


    def get_view_matrix_focused_on(self, target):
        
        return self.look_at(self.camera_pos, target, self.camera_up)

    def get_local_vector(self,vector):
        view = self.look_at(self.camera_pos,self.target,self.camera_up)
        i_view = matrix44.inverse(view.T)
        rot_ = self.mult_mat_vec(i_view,vector)
        return rot_

    def move(self,delta):
        local_delta = self.get_local_vector(delta)
        #print(str(delta/np.linalg.norm(delta))+' n ' + str(np.linalg.norm(delta)) + ':  ' + str(local_delta/np.linalg.norm(local_delta))+' n ' + str(np.linalg.norm(local_delta)))
        self.camera_pos = self.camera_pos + local_delta
        self.target = self.target + local_delta
        self.update_camera_vectors()

    def rotate(self,angle, axis):
        rot_axis = self.get_local_vector(axis)
        vector.normalise(rot_axis)
        rotation_matrix = matrix33.create_from_axis_rotation(rot_axis, angle)
        #print(str(axis)+ ':  ' + str(rot_axis))

        self.camera_front = Vector3(vector3.normalise(self.mult_mat_vec(rotation_matrix, self.camera_pos - self.target)))
        self.target = self.camera_pos - self.camera_front
        self.update_camera_vectors()

    def update_camera_vectors(self):
        self.camera_right = Vector3(vector.normalise(vector3.cross(Vector3([0.0, 1.0, 0.0]),self.camera_front)))
        self.camera_up = Vector3(vector.normalise(vector3.cross( self.camera_front,self.camera_right)))

    def look_at(self, position, target, world_up):
        # 1.Position = known
        # 2.Calculate cameraDirection
        zaxis = vector.normalise(position - target)
        # 3.Get positive right axis vector
        xaxis = vector.normalise(vector3.cross(vector.normalise(world_up), zaxis))
        # 4.Calculate the camera up vector
        yaxis = vector3.cross(zaxis, xaxis)

        # create translation and rotation matrix
        translation = Matrix44.identity()
        translation[3][0] = -position.x
        translation[3][1] = -position.y
        translation[3][2] = -position.z

        rotation = Matrix44.identity()
        rotation[0][0] = xaxis[0]
        rotation[1][0] = xaxis[1]
        rotation[2][0] = xaxis[2]
        rotation[0][1] = yaxis[0]
        rotation[1][1] = yaxis[1]
        rotation[2][1] = yaxis[2]
        rotation[0][2] = zaxis[0]
        rotation[1][2] = zaxis[1]
        rotation[2][2] = zaxis[2]




        return  translation * rotation

    def mult_mat_vec(self,matrix,vector):
        result = np.empty((np.asarray(vector).shape))
        m = np.asarray(matrix)
        v = np.asarray(vector)
        for x in range(len(vector)):
            result[x] = np.sum(v*m[x,:len(vector)])
        return result
