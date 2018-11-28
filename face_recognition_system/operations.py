
import numpy as np
import cv2

#!/usr/bin/env python
# operations.py

def resize(images, size=(100, 100)):
    
    images_norm = []
    for image in images:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # using different OpenCV method if enlarging or shrinking
        if image.shape < size:
            image_norm = cv2.resize(image, size, interpolation=cv2.INTER_AREA)
        else:
            image_norm = cv2.resize(image, size, interpolation=cv2.INTER_CUBIC)
        images_norm.append(image_norm)

    return images_norm


def normalize_intensity(images):
    
    images_norm = []
    for image in images:
        is_color = len(image.shape) == 3
        if is_color:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        images_norm.append(cv2.equalizeHist(image))
    return images_norm


def cut_face_rectangle(image, face_coord):
    
    images_rectangle = []
    for (x, y, w, h) in face_coord:
        images_rectangle.append(image[y: y + h, x: x + w])
    return images_rectangle

def cut_face_ellipse(image, face_coord):
    
    images_ellipse = []
    for (x, y, w, h) in face_coord:
        center = (x + w / 2, y + h / 2)
        axis_major = h / 2
        axis_minor = w / 2
        mask = np.zeros_like(image)
        # create a white filled ellipse
        mask = cv2.ellipse(mask,
                           center=center,
                           axes=(axis_major, axis_minor),
                           angle=0,
                           startAngle=0,
                           endAngle=360,
                           color=(255, 255, 255),
                           thickness=-1)
        # Bitwise AND operation to black out regions outside the mask
        image_ellipse = np.bitwise_and(image, mask)
        images_ellipse.append(image_ellipse[y: y + h, x: x + w])

    return images_ellipse

def draw_face_rectangle(image, faces_coord):
    """ Draws a rectangle around the face found.
    """
    for (x, y, w, h) in faces_coord:
        cv2.rectangle(image, (x, y), (x + w, y + h), (206, 0, 209), 2)
    return image

def draw_face_ellipse(image, faces_coord):
    """ Draws an ellipse around the face found.
    """
    for (x, y, w, h) in faces_coord:
        center = (x + w / 2, y + h / 2)
        axis_major = h / 2
        axis_minor = w / 2
        cv2.ellipse(image,
                    center=center,
                    axes=(axis_major, axis_minor),
                    angle=0,
                    startAngle=0,
                    endAngle=360,
                    color=(206, 0, 209),
                    thickness=2)
    return image
