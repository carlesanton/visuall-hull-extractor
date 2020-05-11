import numpy as np
import matplotlib
matplotlib.use('TKAgg',warn=False, force=True)
from matplotlib import pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

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
    print(np.linalg.eigvalsh(w))

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

def compute_external_params_for_all_images(camera_parameters, all_homographies):
    external_parameters_list = [compute_external_params(camera_parameters,homography) for homography in all_homographies]
    
    return external_parameters_list

def plot_cameras(external_params):
    camera_centers_xs = [ext[1][0] for ext in external_params]
    camera_centers_ys = [ext[1][1] for ext in external_params]
    camera_centers_zs = [ext[1][2] for ext in external_params]

    fig = matplotlib.pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')


    ax.scatter(0,0,0,c='r', marker='o')
    ax.scatter(camera_centers_xs,camera_centers_ys,camera_centers_zs,c='b', marker='^')
    
    #plt.savefig('foo.png')
    matplotlib.pyplot.show()
    a=0

    
    
