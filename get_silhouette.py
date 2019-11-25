import numpy as np
import cv2
import os


#get silhouette of image taken from webcam and process it in order to make it more robust


def pre_process_image(img):
    opening = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel_e)
    erosion = cv2.erode(opening,kernel_e,iterations = 3)
    retval, thresholded = cv2.threshold(opening, threshold, 255, cv2.THRESH_BINARY)
    filtered = cv2.filter2D(thresholded,-1,kernel_f)
    closing = cv2.morphologyEx(filtered, cv2.MORPH_CLOSE, kernel_c)

    return closing
    
if __name__ == "__main__":
    folder_path = 'C:/Users/Carles/Documents/Code/visualhull/get image/captures'
    default_background_folder = 'C:/Users/Carles/Documents/Code/visualhull/get image/background'
    default_background = 'backgroundd.png'


    cap = cv2.VideoCapture(1)

    #load first backgrund
    backSub = cv2.createBackgroundSubtractorKNN()
    background = cv2.imread(os.path.join(default_background_folder,default_background),0)
    threshold = 33
    background_learned = False

    #for image processing, erode etc etc
    kernel_e = np.ones((5,5),np.uint8)
    kernel_c = np.ones((5,5),np.uint8)
    kernel_f = np.ones((5,5),np.float32)/25
    # = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if background_learned:
            absolute_difference = abs(background-gray)
            cv2.imshow('frame',pre_process_image(absolute_difference))
        else: 
            fgMask = backSub.apply(frame)
            cv2.imshow('frame',pre_process_image(fgMask))
            
        '''
        absolute_difference = abs(background-gray)
        retval, thresholded =   cv2.threshold(absolute_difference, threshold, 255, cv2.THRESH_BINARY)
        '''
        # Display the resulting frame
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            image_name='capture_num'+ str(len([n for n in os.listdir(folder_path) if n.endswith('.png')]))+'.png'
            cv2.imwrite(os.path.join(folder_path,image_name),gray) 
            print(image_name + ' saved into ' + folder_path)
        elif key == ord('b'):
            background = frame

            print("New background taken")
        elif key == ord('+'):
            threshold+=1
            print("New threshold = " + str(threshold))
        elif key == ord('-'):
            threshold-=1
            print("New threshold = " + str(threshold))
        elif key == ord('r'):
            background = cv2.cvtColor(backSub.getBackgroundImage(), cv2.COLOR_BGR2GRAY)
            cv2.imwrite(os.path.join(default_background_folder,'backgroundd.png'),background)
            background_learned = not background_learned
        elif key == ord('t'):
            background_learned = not background_learned

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

