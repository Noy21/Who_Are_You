import locations_functions as location
import masks_functions as masks
import skin_functions as skin


class ChangePart:
    def __init__(self, image):
        """
        :param image: the image we want to change.
        """
        self.image = image

    def make_a_change(self, part, function, change_values):
        """
        :param part: the part int the face we want to change.
        :param function: what we want to change - size / place.
        :param change_values: sizes of: (move_right_or_down, enlarge, minimize)
        :return: the image after changing it
        """
        marks = location.find_landmarks(self.image)
        coordinates, center_skin, center_cropped = location.get_six_coordinates(function, marks, part, change_values[0])
        skin_size, cropped_size = location.width_height(function, coordinates, change_values[1], change_values[2])
        skin_mask, part_mask = masks.get_resized_masks(self.image, marks, part, (skin_size, cropped_size))
        area_part_resized, self.image = skin.handle_skin(self.image, cropped_size, skin_size, center_skin, coordinates, skin_mask)
        area_cropped = skin.get_area(self.image, center_cropped, cropped_size[0], cropped_size[1])
        skin.coloring_by_mask(part_mask, area_cropped, area_part_resized, False)
        return self.image

    @staticmethod
    def get_part(part):
        """
        gets the part by the request
        :param part: on of the following strings - NOSE/RIGHT_EYE/LEFT_EYE/MOUTH/FACE
        :return: part = ([landmarks], {"Top":_, "Low":_, "Right": _, "Left": _, "Center": [_,_]})
        """
        if part == "NOSE":
            return [29, 31, 32, 33, 34, 35], {"Top": 29, "Low": 33, "Right": 35, "Left": 31, "Center": [30]}
        elif part == "RIGHT_EYE":
            return [42, 43, 44, 45, 46, 47], {"Top": 44, "Low": 47, "Right": 45, "Left": 42, "Center": [44, 47]}
        elif part == "LEFT_EYE":
            return [36, 37, 38, 39, 40, 41], {"Top": 37, "Low": 40, "Right": 39, "Left": 36, "Center": [38, 41]}
        elif part == "MOUTH":
            return ([48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
                    {"Top": 51, "Low": 57, "Right": 54, "Left": 48, "Center": [62, 66]})
        elif part == "FACE":
            return ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                    {"Top": 27, "Low": 8, "Right": 15, "Left": 1, "Center": [2, 14]})
        return None
