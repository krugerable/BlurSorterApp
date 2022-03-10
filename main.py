# Import the Tkinter library
from tkinter import *
from tkinter import filedialog

# Imports
import os
import shutil
import cv2

root = Tk()

lblFolderName = Label(root, text="No folder selected")
lblStatus = Label(root, text="Status")

lblFolderName.pack()
lblStatus.pack()

FOCUS_THRESHOLD = 80
BLURRED_DIR = 'blurred'
OK_DIR = 'ok'

global folder_selected
global blur_count


def select_folder_clicked():
    folder_selected = filedialog.askdirectory()
    lblFolderName.config(text=folder_selected)
    root.geometry()
    blur_count = 0
    files = [f for f in os.listdir(folder_selected)]  # if f.endswith('.jpg')]

    lblStatus.config(text='Found ' + str(len(files)))

    try:
        os.makedirs(BLURRED_DIR)
        os.makedirs(OK_DIR)
    except:
        pass

    for infile in files:
        lblStatus.config(text='Processing file %s ...' % infile)
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

    lblStatus.config(text='Done.  Processed %d files into %d blurred, and %d ok.' % (
    len(files), blur_count, len(files) - blur_count))

    return


btnSelectFolder = Button(root, text="Select folder with images.", command=select_folder_clicked)
btnSelectFolder.pack()

root.winfo_geometry()

root.mainloop()
