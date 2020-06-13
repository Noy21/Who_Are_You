import cv2
import numpy as np
import masks_functions as masks
import locations_functions as location


def get_area(image, center, width, height):
    """
    gets an image, a center and a size. then, returns the image cut in the place.
    :param image: the original image
    :param center: coordinates of the center of the shape we want to cut (x, y)
    :param width: shape's width
    :param height: shape's height
    :return: an image cut in the shape
    """
    top_left = (int(center[0] - width / 2), int(center[1] - height / 2))
    return image[top_left[1]: top_left[1] + height, top_left[0]: top_left[0] + width]


def avg_color(image, list_of_coordinates):
    """
    gets an image and a few coordinates and returns the average color
    :param image: the original image (in b, g ,r).
    :param list_of_coordinates: a list of skin coordinates [(x,y), (x, y), (x, y)...]
    :return: the average color of this coordinates (b, g, r)
    """
    b, g, r, count = 0, 0, 0, 0
    for coordinate in list_of_coordinates:
        pixel_b, pixel_g, pixel_r = image[coordinate[1], coordinate[0]]
        r += pixel_r
        g += pixel_g
        b += pixel_b
        count += 1
    return int(b / count), int(g / count), int(r / count)


def avg_skin(image, coordinates):
    """
    gets an image and a 4 coordinates. then, returns the average color
    :param image: the original image (in b, g ,r).
    :param coordinates: [top, low, right, left] where each is: (x, y)
    :return: the average color of this coordinates (b, g, r)
    """
    top, low, right, left = coordinates
    skin_coordinates = ((top[0], int(top[1] * 0.9)),
                        (low[0], int(low[1] * 1.1)),
                        (int(right[0] * 1.1), right[1]),
                        (int(left[0] * 0.9), left[1]))
    skin_coordinates = location.get_bounding_rectangle_coordinates(skin_coordinates)
    return avg_color(image, skin_coordinates)


def skin_color_blank(image, coordinates, size):
    """
    given an image, 4 points, a mask, and coordinates, returns a blank colored mask in the size
    :param image: the original image
    :param coordinates: [top, low, right, left] where each is: (x, y)
    :param size: skin's size (width, height)
    :return: the cropped picture
    """
    blank_image = masks.get_mask(image.shape)
    blank_image[:] = avg_skin(image, coordinates)
    return cv2.resize(blank_image, size)


def coloring_by_mask(mask, area, resized_image, needs_blur):
    """
    coloring an area where the mask is contoured by the resized image's pixels.
    :param mask: the mask that tells where to color.
    :param area: the area that needs to bo colored.
    :param resized_image: the image used to color the area.
    :param needs_blur: a boolean value that represents if the area needs a blur.
    :return: affects the area as a colored area
    """
    width, height, chanel = area.shape
    for x in range(width):
        for y in range(height):
            if mask[x, y] > 200:
                area[x, y] = resized_image[x, y]
    area = cv2.blur(area, (20, 10)) if needs_blur else area


def blur_area(image, center_skin, skin_size):
    """
    blur a image with an ellipse shape
    :param image: the image that needs a blur
    :param center_skin: coordinates of the center of the shape we want to blur (x, y)
    :param skin_size:the skin's size (width, height)
    :return: the image after blurring
    """
    blurred_img = cv2.GaussianBlur(image, (41, 41), 0)  # (41, 41) = 41% blur
    mask = masks.get_mask(image.shape)
    mask = cv2.ellipse(mask, center_skin, (int(skin_size[0]/2), int(skin_size[1]/2)), 0, 0, 360, (255, 255, 255), -1)
    return np.where(mask != np.array([255, 255, 255]), image, blurred_img)


def handle_skin(image, cropped_size, skin_size, center_skin, coordinates, skin_mask):
    """
    gets an image, crop and resize the wanted area, then paste a colored image on the original.
    :param image: the original image, that would get colored in the skin color
    :param cropped_size: # changed! line 109. the size of the cropped image (width, height)
    :param skin_size: the skin's size (width, height).
    :param center_skin: the part's center's coordinates (x, y).
    :param coordinates: [top, low, right, left] where each is: (x, y)
    :param skin_mask: the mask that tells where to color.
    :return: (the resized part, the image after blurring)
    """
    area_skin = get_area(image, center_skin, skin_size[0], skin_size[1])
    area_part_resized = cv2.resize(area_skin, cropped_size)  # resize part
    skin_color = skin_color_blank(image, coordinates, skin_size)
    coloring_by_mask(skin_mask, area_skin, skin_color, True)

    return area_part_resized, blur_area(image, center_skin, skin_size)

