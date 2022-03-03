#
# Sorts pictures in current directory into two subdirs, blurred and ok
#

import os
import shutil
import cv2

FOCUS_THRESHOLD = 80
BLURRED_DIR = 'blurred'
OK_DIR = 'ok'

blur_count = 0
files = [f for f in os.listdir('.') if f.endswith('.jpg')]

try:
    os.makedirs(BLURRED_DIR)
    os.makedirs(OK_DIR)
except:
    pass

for infile in files:

    print('Processing file %s ...' % infile)
    cv_image = cv2.imread(infile)

    # Covert to grayscale
    gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

    # Compute the Laplacian of the image and then the focus
    #     measure is simply the variance of the Laplacian
    variance_of_laplacian = cv2.Laplacian(gray, cv2.CV_64F).var()

    # If below threshold, it's blurry
    if variance_of_laplacian < FOCUS_THRESHOLD:
        shutil.move(infile, BLURRED_DIR)
        blur_count += 1
    else:
        shutil.move(infile, OK_DIR)

print('Done.  Processed %d files into %d blurred, and %d ok.' % (len(files), blur_count, len(files) - blur_count))
