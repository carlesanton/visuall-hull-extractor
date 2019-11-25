import pygame
from pygame.locals import *
import numpy as np
import time
from Camera import Camera
from pyrr import Vector3, matrix44, vector, vector3


from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


#3d enviroment where visual hull wll be represented



verticies = (
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    )
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )


world_size = 50
line_spacing = 4
cam = Camera([0.0,0.5,10.0], [0.0,0.5,0.0])#position=[0.0,-0.5,5] , target=[0.0,0.0,0.0]


ground_points = np.linspace(-world_size/2, world_size/2, world_size/line_spacing, endpoint=True)



def check_boundaries():

    # print(camera_x,camera_y,camera_z)
    # Y boundaries
    if cam.camera_pos.y<0.5:
        cam.camera_pos.y = 0.5
    if cam.camera_pos.y>world_size:
        cam.camera_pos.y = world_size
        
    # X boundaries
    if cam.camera_pos.x<-world_size/2:
        cam.camera_pos.x = -world_size/2

    if cam.camera_pos.x>world_size/2:
        cam.camera_pos.x = world_size/2

    # Z boundaries
    if cam.camera_pos.z<-world_size/2:
        cam.camera_pos.z = -world_size/2
    if cam.camera_pos.z>world_size/2:
        cam.camera_pos.z = world_size/2


    cam.target = cam.camera_pos - cam.camera_front
    cam.update_camera_vectors()

def Cube():
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def ground():
    glBegin(GL_LINES)
    glColor3f(1.0,1.0,1.0)
    
    # #############################################
    # ground lines
    for line in ground_points:
        
        # vertical lines
        glVertex3fv((line,0,world_size/2))
        glVertex3fv((line,0,-world_size/2))
        # horizontal lines
        glVertex3fv((world_size/2,0, line))
        glVertex3fv((-world_size/2,0,line))

        # #############################################
        # roof lines
        # vertical lines
        glVertex3fv((line,world_size,world_size/2))
        glVertex3fv((line,world_size,-world_size/2))
        # horizontal lines
        glVertex3fv((world_size/2,world_size, line))
        glVertex3fv((-world_size/2,world_size,line))

        # #############################################
        # front wall lines
        # vertical lines
        glVertex3fv((line,world_size,-world_size/2))
        glVertex3fv((line,0,-world_size/2))
        # horizontal lines
        glVertex3fv((world_size/2,line+world_size/2, -world_size/2))
        glVertex3fv((-world_size/2,line+world_size/2,-world_size/2))

        # #############################################
        # back wall lines
        # vertical lines
        glVertex3fv((line,world_size,world_size/2))
        glVertex3fv((line,0,world_size/2))
        # horizontal lines
        glVertex3fv((world_size/2,line+world_size/2, world_size/2))
        glVertex3fv((-world_size/2,line+world_size/2,world_size/2))
        
        # #############################################
        # right wall lines
        # vertical lines
        glVertex3fv((-world_size/2,world_size,line))
        glVertex3fv((-world_size/2,0,line))
        # horizontal lines
        glVertex3fv((-world_size/2,line+world_size/2, -world_size/2))
        glVertex3fv((-world_size/2,line+world_size/2, world_size/2))
    
        # #############################################
        # left wall lines
        # vertical lines
        glVertex3fv((world_size/2,world_size,line))
        glVertex3fv((world_size/2,0,line))
        # horizontal lines
        glVertex3fv((world_size/2,line+world_size/2, -world_size/2))
        glVertex3fv((world_size/2,line+world_size/2, world_size/2))

    glEnd()



def plot_axes():
    glBegin(GL_LINES)
    # red X axis
    glColor3f(1.0,0.0,0.0)
    glVertex3fv([0.0,0.0,0.0])
    glVertex3fv([1.0,0.0,0.0])
    # green Y axis
    glColor3f(0.0,1.0,0.0)
    glVertex3fv([0.0,0.0,0.0])
    glVertex3fv([0.0,1.0,0.0])
    # blue Z axis
    glColor3f(0.0,0.0,1.0)
    glVertex3fv([0.0,0.0,0.0])
    glVertex3fv([0.0,0.0,1.0])

    glEnd()

def proces_mouse(prev_pos_x,prev_pos_y,is_mouse_down):
    #get mouse position and delta (do after pump events)
    (pos_x,pos_y) = pygame.mouse.get_pos()
    #compute delta of previous and actual position
    mouse_delta_x = (prev_pos_x-pos_x)
    mouse_delta_y = (prev_pos_y-pos_y)
    #print(str(mouse_delta_x) + ' ' + str(mouse_delta_y))
    #store new position



    # si el boto esquerra està clicat

    if is_mouse_down:
        # rotate the pertinent amount in each axis
        cam.rotate(-mouse_delta_x*cam.rot_step, Vector3([.0,1.0,.0]))
        cam.rotate(-mouse_delta_y*cam.rot_step, Vector3([1.0,.0,.0]))

    return pos_x, pos_y

def proces_keyboard():
    keys = pygame.key.get_pressed()
    #print(cam.speed)
    if keys[pygame.K_LEFT]:
        cam.move([-1.0* cam.speed,.0* cam.speed,.0* cam.speed])        
    if keys[pygame.K_RIGHT]:
        cam.move([1.0* cam.speed,.0* cam.speed,.0* cam.speed])       
    if keys[pygame.K_UP]:
        cam.move([.0* cam.speed,.0* cam.speed,-1.0* cam.speed])
    if keys[pygame.K_DOWN]:
        cam.move([.0* cam.speed,.0* cam.speed,1.0* cam.speed])

    if keys[pygame.K_a]:
        cam.rotate(-cam.rot_step,Vector3([0.0,1.,.0]))
    if keys[pygame.K_s]:
        cam.rotate(cam.rot_step,Vector3([1.0,0.0,.0]))
    if keys[pygame.K_d]:
        cam.rotate(cam.rot_step,Vector3([0.0,1.0,.0]))
    if keys[pygame.K_w]:
        cam.rotate(-cam.rot_step,Vector3([1.0,0.0,.0]))

def plot_cam_axes():
    
    ofset = Vector3(cam.camera_pos-cam.camera_front*10)
    #ofset = Vector3([1.0,1.0,1.0])
    glBegin(GL_LINES)
    # red X axis
    glColor3f(1.0,0.0,0.0)
    glVertex3fv([ofset.x,ofset.y,ofset.z])
    glVertex3fv([cam.camera_right.x+ofset.x,cam.camera_right.y+ofset.y,cam.camera_right.z+ofset.z])
    # green Y axis
    glColor3f(0.0,1.0,0.0)
    glVertex3fv([ofset.x,ofset.y,ofset.z])
    glVertex3fv([cam.camera_up.x+ofset.x,cam.camera_up.y+ofset.y,cam.camera_up.z+ofset.z])
    # blue Z axis
    glColor3f(0.0,0.0,1.0)
    glVertex3fv([ofset.x,ofset.y,ofset.z])
    glVertex3fv([cam.camera_front.x+ofset.x,cam.camera_front.y+ofset.y,cam.camera_front.z+ofset.z])

    #plot camera front begining from 0.0 0.0 0.0
    glColor3f(1.0,1.0,1.0)
    glVertex3fv([.0,.0,.0])
    glVertex3fv([-cam.camera_front.x,-cam.camera_front.y,-cam.camera_front.z])
   

    glEnd()




def main():
    pygame.init()
    display = (800,600)
    background_show = True
    ttt = time.time()
    show_time = True
    is_mouse_down = False


    print_pos = False
    print_modelview = False
    #store initial mouse position
    (mouse_pos_x,mouse_pos_y) = pygame.mouse.get_pos()

    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)


    # prespective =  matrix44.create_perspective_projection(45, (display[0]/display[1]), 0.1, 500.0) 
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (display[0]/display[1]), 0.1, 500.0)
    while True:
        pygame.time.delay(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            # keyboard key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    background_show = not  background_show
                
                if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                    cam.speed = cam.speed*4
                

            # mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN:
                # left click
                if event.button == 1:
                    is_mouse_down = True


            # mouse button up
            if event.type == pygame.MOUSEBUTTONUP:
                # right click
                if event.button == 1:
                    is_mouse_down = False
        

        (mouse_pos_x, mouse_pos_y) = proces_mouse(mouse_pos_x, mouse_pos_y, is_mouse_down)
        proces_keyboard()
        check_boundaries()
        glMatrixMode (GL_MODELVIEW)
        glLoadIdentity()
        #glLoadMatrixf(cam.get_view_matrix())
        #glTranslate(-cam.camera_pos.x,-cam.camera_pos.y,-cam.camera_pos.z)
        cam.cam_lookat()
        if print_modelview:
            a = (GLfloat * 16)()
            mvm = glGetFloatv(GL_MODELVIEW_MATRIX, a)
            print('GL look at matrix: ')
            print(np.asarray(list(a)).reshape((4,4)))
            print('--------------')
            print('Computed look at matrix: ')
            print(cam.get_view_matrix())
            print('Camera position: ' + str(cam.camera_pos))
            print('----------------------------')
        if print_pos:
            print(str(cam.camera_pos) + ' ||||x ' + str(cam.camera_right) + ' ||||y ' +str(cam.camera_up) + ' ||||z ' + str(cam.camera_front))
        
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        plot_axes()
        plot_cam_axes()
        if background_show:
            ground()
        pygame.display.flip()

        if show_time:
            d_t = time.time() - ttt
            frame_rate = 1/(d_t)
            print('Time between frames: ' + str('{:06.4f}'.format(d_t)) + ' s || Frame rate: ' +str(frame_rate) + ' fps')
            ttt = time.time()

        ##pygame.time.wait(10)


main()