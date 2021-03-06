import cv2
import numpy as np

"""
Demonstrates how to superimpose an RGBA image on top of an RGB image.
Lots of references from all over the place...


http://docs.opencv.org/trunk/doc/py_tutorials/py_core/py_basic_ops/py_basic_ops.html
http://jepsonsblog.blogspot.hk/2012/10/overlay-transparent-image-in-opencv.html
http://docs.opencv.org/trunk/doc/py_tutorials/py_gui/py_image_display/py_image_display.html
"""
def superimpose(bg_img, fg_img, width_scaling, height_scaling, row_offset, col_offset):

    # Resize the foreground image as needed
    # http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_imgproc/py_geometric_transformations/py_geometric_transformations.html
    height, width = fg_img.shape[:2]
    resized_fg = cv2.resize(fg_img,(int(width*width_scaling), int(height*height_scaling)))

    # Go through the pixels in the fg image
    # if fg pixel is not transparent, add it to the background image with the offset
    # Seems stupid but cv2.add doesn't work with images of different size.
    fg_rows, fg_cols, fg_channels = resized_fg.shape
    for row in range(0,fg_rows):
        for col in range(0, fg_cols):
            if resized_fg[row][col][3] > 0:  # 4th channel is alpha, > 0 is non-transparent
                # background image doesn't have alpha channel, so only copy over rgb channels
                bg_img[row_offset+row][col_offset+col] =resized_fg[row][col][:3] 

    # and show
    return bg_img

