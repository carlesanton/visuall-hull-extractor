import numpy as np
import cv2
import os


#get silhouette of image taken from webcam and process it in order to make it more robust

def stack_images_horizontaly(image_list):
    stacked_image = image_list.pop(0)
    for image in image_list:
        stacked_image = np.hstack((np.array(stacked_image, dtype = np.uint8), np.array(image, dtype = np.uint8)))

    return stacked_image


def stack_images_verticaly(image_list):
    stacked_image = image_list.pop(0)
    for image in image_list:
        stacked_image = np.vstack((np.array(stacked_image, dtype = np.uint8), np.array(image, dtype = np.uint8)))

    return stacked_image


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


    cap = cv2.VideoCapture(2)

    #load first backgrund
    backSub = cv2.createBackgroundSubtractorKNN()
    background = cv2.imread(os.path.join(default_background_folder,default_background),0)
    threshold = 50
    background_learned = False

    #for image processing, erode etc etc
    kernel_e = np.ones((5,5),np.uint8)
    kernel_c = np.ones((5,5),np.uint8)
    kernel_f = np.ones((5,5),np.float32)/25
    # = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame = np.array(frame, dtype=np.int16)
        gray = np.array(gray, dtype=np.int16)
        
        if background_learned:
            absolute_difference = abs(frame-background)
            retval, mask = cv2.threshold(absolute_difference, threshold, 255, cv2.THRESH_BINARY)
       

            row_1 = stack_images_horizontaly([mask, absolute_difference])
            row_2 = stack_images_horizontaly([frame, background])
            multiview = stack_images_verticaly([row_1, row_2])  
            cv2.putText(img = multiview, text = f'threshold: {threshold}',org = (30,50), fontFace = cv2.FONT_HERSHEY_SIMPLEX , fontScale = 0.5, color = (0,0,255), thickness = 1)
            cv2.imshow('frame',multiview)

            
        else: 
            fgMask = backSub.apply(frame)
            cv2.imshow('frame',fgMask)
            

        # Display the resulting frame
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == ord('c'):
            image_name='capture_num'+ str(len([n for n in os.listdir(folder_path) if n.endswith('.png')]))+'.png'
            cv2.imwrite(os.path.join(folder_path,image_name),gray) 
            print(image_name + ' saved into ' + folder_path)
        elif key == ord('b'):
            background = np.array(frame, dtype = np.uint8)
            gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
            
            background = np.array(background, dtype=np.int16)
            gray_background = np.array(gray_background, dtype=np.int16)
            
            cv2.imwrite(os.path.join(default_background_folder,'backgroundd.png'),background)
            background_learned = True


            background_learned = True
            print("New background taken")
        elif key == ord('+'):
            threshold+=1
            print("New threshold = " + str(threshold))
        elif key == ord('-'):
            threshold-=1
            print("New threshold = " + str(threshold))
        elif key == ord('r'):
            background = backSub.getBackgroundImage()
            gray_background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
            
            background = np.array(background, dtype=np.int16)
            gray_background = np.array(gray_background, dtype=np.int16)
            
            cv2.imwrite(os.path.join(default_background_folder,'backgroundd.png'),background)
            background_learned = True
        elif key == ord('t'):
            background_learned = not background_learned

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

