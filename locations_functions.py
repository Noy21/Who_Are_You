import cv2
import dlib
import math


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("dat_files/shape_predictor_68_face_landmarks.dat")
ENLARGE_SKIN = 1.25


def find_landmarks(image):
    """
    The function finds the important landmarks of the face
    :param image: face image
    :return: the landmarks of the face
    """
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # change to grayscale
    face = detector(gray_img)  # find face - returns a list
    landmarks = predictor(gray_img, face[0])  # find the landmarks - returns an object
    return landmarks


def get_coordinates_by_part(landmarks, part):
    """
    :param landmarks: the face's landmarks
    :param part: the index of the part of the face we want its location
    :return: the coordinates of the part. (x, y)
    """
    mark = landmarks.part(part)
    return mark.x, mark.y


def center_coordinates(landmarks, part):
    """
    finds the coordinates of the part's center
    :param landmarks: face's landmarks
    :param part: the part we wants its center
    :return: the coordinates (x, y) of the center
    """
    center = part["Center"]
    x, y = 0, 0
    for i in center:
        i_x, i_y = get_coordinates_by_part(landmarks, i)
        x += i_x
        y += i_y
    return int(x / len(center)), int(y / len(center))


def move_center(function, center, move_right_or_down):
    """
    move the center if it should be moved
    :param function: the changing's function. if - right/left/up/down change accordingly, else - don't change the center
    :param center: coordinates (x, y) of the part's center
    :param move_right_or_down: a value between -> 1.01 - 1.035, that represents how much to move
    :return: coordinates (x, y) of the part's center after changes
    """
    if function == "Right":
        center = int(center[0] * move_right_or_down), center[1]
    elif function == "Left":
        center = int(center[0] * (2 - move_right_or_down)), center[1]
    elif function == "Up":
        center = center[0], int(center[1] * (2 - move_right_or_down))
    elif function == "Down":
        center = center[0], int(center[1] * move_right_or_down)
    return center


# returns the top, low, right, left, skin center and actual center - (x, y)
def get_six_coordinates(function, landmarks, part, move_right_or_down):
    """
    returns the coordinates of: top, low, right, left, skin center and the crop's center
    :param function: the changing's function.
    :param landmarks: the face's landmarks
    :param part: the part of the face we want its important indexes
    :param move_right_or_down:a value between -> 1.01 - 1.035, that represents how much to move
    :return: ((top_x, top_y), (low_x, low_y), (right_x, right_y), (left_X, left_y)),
             (skin_center_x, skin_center_y), (part_center_x, part_center_y)
    """
    part = part[1]
    top = get_coordinates_by_part(landmarks, part["Top"])
    low = get_coordinates_by_part(landmarks, part["Low"])
    right = get_coordinates_by_part(landmarks, part["Right"])
    left = get_coordinates_by_part(landmarks, part["Left"])
    center = center_coordinates(landmarks, part)
    return (top, low, right, left), center, move_center(function, center, move_right_or_down)


def change_size_if_needed(function, width, height, enlarge, minimize):
    """
    if the function requires changing
    :param function: the changing's function. if Enlarge/Minimize/Elongate/Shorten change size
    :param width: the original width
    :param height: the original height
    :param enlarge: a value between -> 1.09 - 1.25 that represents by how much to enlarge
    :param minimize: a value between -> 0.88 - 0.98 that represents by how much to minimize
    :return: the size after the changes, (x, y)
    """
    if function == "Enlarge":
        width *= enlarge
        height *= enlarge
    elif function == "Minimize":
        width *= minimize
        height *= minimize
    elif function == "Elongate":
        width *= minimize
        height *= enlarge
    elif function == "Shorten":
        width *= enlarge
        height *= minimize
    return int(width), int(height)


def width_height(function, coordinates, enlarge, minimize):
    """
    returns the skin's size (width, height) and the cropped image's size (width, height)
    :param function: the changing's function.
    :param coordinates: ((top_x, top_y), (low_x, low_y), (right_x, right_y), (left_X, left_y))
    :param enlarge: a value between -> 1.09 - 1.25 that represents by how much to enlarge
    :param minimize: a value between -> 0.88 - 0.98 that represents by how much to minimize
    :return: skin's size (width, height), cropped image's size (width, height)
    """
    # distance - right and left
    width = int(ENLARGE_SKIN * math.hypot(coordinates[3][0] - coordinates[2][0], coordinates[3][1] - coordinates[2][1]))
    # distance - top and low
    height = int(ENLARGE_SKIN * math.hypot(coordinates[0][0] - coordinates[1][0], coordinates[0][1] - coordinates[1][1]))
    return (width, height), change_size_if_needed(function, width, height, enlarge, minimize)


def get_bounding_rectangle_coordinates(skin_coordinates):
    """
    gets 4 skin coordinates and returns the coordinates of the bounding rectangle
    :param skin_coordinates: (top, low, right, left) coordinates where each is: (x, y)
    :return: a list of coordinates: [(x, y), (x, y), (x, y)...]
    """
    top, low, right, left = skin_coordinates
    x_start, x_end = left[0], right[0]
    y_start, y_end = top[1], low[1]
    coordinates = [top, low, right, left]
    for x in range(x_start, x_end):
        coordinates.append((x, y_start))
        coordinates.append((x, y_end))
    for y in range(y_start, y_end):
        coordinates.append((x_start, y))
        coordinates.append((x_end, y))
    return coordinates
