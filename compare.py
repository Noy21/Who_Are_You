import face_recognition
import math


FACE_MATCH_THRESHOLD = 0.6


class Compare:
    def __init__(self, image_1, image_2):
        """
        :param image_1: the first image we want to compare
        :param image_2: the second image we want to compare
        """
        self.image_1 = image_1
        self.image_2 = image_2
        self.distance = self.compare_two_images()
        self.decimal = Compare.distance_to_decimal(self.distance)
        self.percents = Compare.change_to_percents(self.decimal)

    def compare_two_images(self):
        """
        compares self.image_1 to self.image_2.
        :return: the distance between the 2 of them.
        """
        self.image_1 = self.get_encoded_image(self.load(self.image_1))
        self.image_2 = self.get_encoded_image(self.load(self.image_2))
        return face_recognition.face_distance([self.image_1], self.image_2)

    def get_percents(self):
        """
        :return: the similarity percents
        """
        return self.percents

    @staticmethod
    def distance_to_decimal(face_distance):
        """
        translates the distance to a float number.
        :param face_distance: the distance between the images.
        :return: the decimal represents the distance.
        """
        if face_distance > FACE_MATCH_THRESHOLD:
            face_range = (1.0 - FACE_MATCH_THRESHOLD)
            linear_val = (1.0 - face_distance) / (face_range * 2.0)
            return linear_val
        else:
            face_range = FACE_MATCH_THRESHOLD
            linear_val = 1.0 - (face_distance / (face_range * 2.0))
            return linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))

    @staticmethod
    def change_to_percents(distance):
        """
        translate the decimal distance to percents
        :param distance: the decimal represents the distance.
        :return: percents of the distance.
        """
        distance = distance[0] * 100
        return round(distance, 2)

    @staticmethod
    def get_encoded_image(image):
        """
        :param image: the image we want to encode
        :return: the encoding image
        """
        return face_recognition.face_encodings(image)[0]

    @staticmethod
    def load(image):
        """
        :param image: the image we want to load
        :return: face loaded
        """
        return face_recognition.load_image_file(image)
