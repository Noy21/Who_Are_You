import cv2
import locations_functions
import numpy as np


def get_points(landmarks, part):
    """
    gets the landmarks of the face and a list of what part to notice and returns a list of the marks
    :param landmarks: the landmarks of the face
    :param part: the face's part we want its shape
    :return: a list of the marks in np.array type: [[[(x,y), (x,y)...]]]
    """
    marks = []
    for a_part in part[0]:
        marks.append((locations_functions.get_coordinates_by_part(landmarks, a_part)))
    return np.array([marks])


def get_mask(image_shape):
    """
    return a new array of given shape, filled with zeros
    :param image_shape: the shape of the image
    :return: a new array filled with zeros
    """
    return np.zeros(image_shape, dtype=np.uint8)


def get_mask_contours(image, points):
    """
    creates a mask, draws contours, then returns the mask
    :param image: the image we want its masks and contours
    :param points: the points of the shape
    :return: a drawn mask
    """
    mask = get_mask(image.shape[0:2])    # draw a mask of the shape
    cv2.drawContours(mask, [points], -1, (255, 255, 255), -1, cv2.LINE_AA)    # draw contour of shape
    return mask


def crop_area(image, points):
    """
    crop by the shape of the mask and returns the cropped picture
    :param image: the image we want to crop
    :param points: the points of the shape
    :return: cropped rectangle of the image in the required points
    """
    rect = cv2.boundingRect(points)  # returns (x,y,w,h) of the rect
    return image[rect[1]: rect[1] + rect[3], rect[0]: rect[0] + rect[2]]


def get_resized_masks(image, marks, part, sizes):
    """
    creates 2 masks (skin, cropped image) and returns them
    :param image: the face's image
    :param marks: the landmarks of the face
    :param part: the face's part we want its shape
    :param sizes: (skin_size, cropped_size) where each size is: (width, height)
    :return: skin's resized mask, cropped image's resized mask
    """
    points = get_points(marks, part)  # gets the points
    mask = get_mask_contours(image, points)  # contour the points and creates a mask
    mask = crop_area(mask, points)
    return cv2.resize(mask, sizes[0]), cv2.resize(mask, sizes[1])

