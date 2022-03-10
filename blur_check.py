# import required module
import os
import shutil
import cv2
import pathlib

#Constants
FOCUS_THRESHOLD = 20
BLURRED_DIR = 'blurred'
OK_DIR = 'ok'
CURR_DIR = os.path.dirname(os.path.realpath(__file__))
print(CURR_DIR)
blur_count = 0

try:
    os.makedirs(BLURRED_DIR)
    os.makedirs(OK_DIR)
except:
    pass


# iterate over files in
# that directory
for filename in os.listdir(CURR_DIR):
        f = os.path.join(CURR_DIR, filename)
        if f.endswith('.JPG'):
            
            print(f)

            #cv_image = cv2.imread(f)

            # Covert to grayscale
            gray = cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2GRAY)

            # Compute the Laplacian of the image and then the focus
            #     measure is simply the variance of the Laplacian
            variance_of_laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

            # If below threshold, it's blurry
            if variance_of_laplacian < FOCUS_THRESHOLD:
                shutil.move(f, BLURRED_DIR)
                blur_count += 1
            else:
                shutil.move(f, OK_DIR)
                print(f)
