import cv2
import numpy as np

"""
Demonstrates how to superimpose an RGBA image on top of an RGB image.
Lots of references from all over the place...


http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
http://jepsonsblog.blogspot.hk/2012/10/overlay-transparent-image-in-opencv.html
http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_image_display/py_image_display.html
"""
def cover(bg_img, fg_img, width_scaling, height_scaling, row_offset, col_offset):
    # Resize the foreground image as needed
    # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
    height, width = fg_img.shape[:2]
    resized_fg = cv2.resize(fg_img,(int(width*width_scaling), int(height*height_scaling)))

    # Go through the pixels in the fg image
    # if fg pixel is not transparent, add it to the background image with the offset
    # Seems stupid but cv2.add doesn't work with images of different size.
    fg_rows, fg_cols, fg_channels = resized_fg.shape
   
    bg_img[row_offset:row_offset+fg_rows,col_offset:col_offset+fg_cols] = resized_fg   
 
    # and show
    return bg_img



