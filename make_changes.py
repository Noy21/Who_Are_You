import change_a_part
import random
import cv2


PARTS = ["NOSE", "RIGHT_EYE", "LEFT_EYE", "MOUTH", "FACE"]
FUNCTIONS = ["Enlarge", "Minimize", "Elongate", "Shorten", "Right", "Left", "Up", "Down"]
PARTS_RANGE_VALUES = {"right_down": (1.01, 1.035), "enlarge": (1.09, 1.25), "minimize": (0.88, 0.98)}
FACE_RANGE_VALUES = {"enlarge": (0.98, 1.18), "minimize": (0.98, 1.02)}


class MakeChanges:
    def __init__(self, image, num_of_changes=3):
        """
        :param image: the url of the image we want to change
        :param num_of_changes: the number of changes we would like
        """
        self.image = cv2.imread(image)  # open picture as cv2 image
        self.width, self.height, self.image = MakeChanges.resize_before(self.image)
        self.change = change_a_part.ChangePart(self.image)
        self.num_of_changes = num_of_changes

    def make_all_changes(self):
        """
        chooses random parts, random functions and random change values.
        then makes all the changes.
        :return: the changed image after resizing it to the original size.
        """
        parts = MakeChanges.get_parts(self.num_of_changes - 1)
        functions = MakeChanges.get_functions(self.num_of_changes - 1)
        range_values = MakeChanges.decide_range(parts[0])
        for change_index in range(len(parts)):
            part, function = parts[change_index], functions[change_index]
            self.change_part(part, function, range_values)
            print(part, function, range_values)
        self.change_face_shape(MakeChanges.decide_range("FACE"))
        return MakeChanges.resize_after(self.image, self.width, self.height)

    def change_part(self, part, function, change_values):
        """
        make a single change on the image
        :param part: a string that represents the part we want to change.
        :param function: a string that represents the function, how we want to change.
        :param change_values: sizes of: (move_right_or_down, enlarge, minimize)
        """
        part = change_a_part.ChangePart.get_part(part)
        self.image = self.change.make_a_change(part, function, change_values)

    def change_face_shape(self, change_values):
        """
        changes the face shape
        :param change_values: sizes of: (move_right_or_down, enlarge, minimize)
        """
        self.change_part("FACE", "Elongate", change_values)

    @staticmethod
    def get_value_by_range(min_and_max, round_num=3):
        """
        get a random number float number, rounded by a chosen number
        :param min_and_max: a tuple of min and max values
        :param round_num: how many number after the ".", the default is 3
        :return: a random float number
        """
        return round(random.SystemRandom().uniform(min_and_max[0], min_and_max[1]), round_num)

    @staticmethod
    def get_parts(num_of_changes):
        """
        get the parts we would like to change.
        :param num_of_changes: the number of changes we want.
        :return: a list of strings that represent the parts. ["string", "string"...]
        """
        parts = []
        for i in range(num_of_changes):
            index = int(MakeChanges.get_value_by_range((0, len(PARTS)-1)))
            parts.append(PARTS[index])  # we subtract 1 to avoid "FACE"
        return parts

    @staticmethod
    def get_functions(num_of_changes):
        """
        get the functions we would like to change.
        :param num_of_changes: the number of changes we want.
        :return: a list of strings that represent the functions. ["string", "string"...]
        """
        functions = []
        for i in range(num_of_changes):
            func = MakeChanges.get_value_by_range((0, len(FUNCTIONS) - 1), 0)
            functions.append(FUNCTIONS[int(func)])
        return functions

    @staticmethod
    def decide_range(part):
        """
        decides the change values
        :param part: what part of the face we want to change.
        :return: sizes of: (move_right_or_down, enlarge, minimize)
        """
        if part == "FACE":
            return MakeChanges.face_decide_range()
        return MakeChanges.parts_decide_range()

    @staticmethod
    def face_decide_range():
        """
        handle the face's change values.
        :return: sizes of: (move_right_or_down, enlarge, minimize) where the first is always 1.
        """
        enlarge = MakeChanges.get_value_by_range(FACE_RANGE_VALUES["enlarge"])
        ratio = MakeChanges.get_ratio(enlarge, FACE_RANGE_VALUES["enlarge"])
        difference_minimize = abs(FACE_RANGE_VALUES["minimize"][1] - FACE_RANGE_VALUES["minimize"][0])
        minimize = round(ratio * difference_minimize, 3) + min(FACE_RANGE_VALUES["minimize"])
        return 1, enlarge, minimize  # we never move the face sideways, so we can return 1

    @staticmethod
    def get_ratio(selection, range_values):
        """
        gets the ratio of a number
        :param selection: the number
        :param range_values: min and max values of the selection
        :return: the ratio
        """
        difference_sum = abs(range_values[1] - range_values[0])
        selection_min = min(range_values)
        return (selection - selection_min) / difference_sum

    @staticmethod
    def parts_decide_range():
        """
        handle the change values of all the parts except the face.
        :return: sizes of: (move_right_or_down, enlarge, minimize)
        """
        right_down = MakeChanges.get_value_by_range(PARTS_RANGE_VALUES["right_down"])
        enlarge = MakeChanges.get_value_by_range(PARTS_RANGE_VALUES["enlarge"])
        total = PARTS_RANGE_VALUES["right_down"][1] + PARTS_RANGE_VALUES["enlarge"][1] + PARTS_RANGE_VALUES["minimize"][0]
        minimize = round(total - right_down - enlarge, 3)
        if minimize > PARTS_RANGE_VALUES["minimize"][1]:
            minimize = PARTS_RANGE_VALUES["minimize"][1]
        return right_down, enlarge, minimize

    @staticmethod
    def resize(img, height, scale):
        """
        resize an image
        :param img: the image we want to resize
        :param height: the height we would like
        :param scale: the ratio between the height and the width
        :return: the resized image
        """
        width = int(height * scale)
        return cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    @staticmethod
    def resize_before(img):
        """
        resize to a default height size and get the original's size
        :param img:
        :return:
        """
        width, height = img.shape[1], img.shape[0]
        ratio = width / height
        return width, height, MakeChanges.resize(img, 1000, ratio)

    @staticmethod
    def resize_after(img, width, height):
        return MakeChanges.resize(img, height, (width / height))
