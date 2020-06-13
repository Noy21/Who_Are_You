from make_changes import *
from compare import *
import os, cv2


class ChangeAllPhotos:
    def __init__(self, compare_name_short):
        """
        :param compare_name_short: the name of the image's file name (without the extension)
        """
        self.path = "uploads/"
        self.static = "static/"
        self.dst_path = "images/uploads_changed/"
        self.compare_name = self.path + ChangeAllPhotos.find_compare_name(self.path, compare_name_short)
        self.list_of_compares = []  # [(img_url, x%, y%), (img_url, x%, y%)...]

    def change_all(self):
        """
        changes all the images, compares them to the compare image (before and after)
        :return: a list of tuples where each tuple contains image url and the 2 percents [(img_url, x%, y%), ...]
        """
        ChangeAllPhotos.delete_all(self.static + self.dst_path)
        compare_name_short = os.path.splitext(self.compare_name)[0].split("/")[1]
        for photo in os.listdir(self.path):
            if os.path.splitext(photo)[0] != compare_name_short:
                print(self.path+photo, self.compare_name)
                distance = Compare(self.path+photo, self.compare_name).get_percents()
                changed_img = MakeChanges(self.path+photo, 4).make_all_changes()
                url = self.static + self.dst_path + photo
                cv2.imwrite(url, changed_img)
                after_distance = Compare(url, self.compare_name).get_percents()
                self.list_of_compares.append((self.dst_path + photo, distance, after_distance))
        ChangeAllPhotos.delete_all(self.path)
        return self.list_of_compares

    @staticmethod
    def delete_all(path):
        """
        deletes all the files in a directory
        :param path: the path to the directory
        """
        for img in os.listdir(path):
            os.remove(path+img)

    @staticmethod
    def find_compare_name(path, compare_name_short):
        """
        finds the compare name (including the extension)
        :param path: the directory's path.
        :param compare_name_short: the compare name (without the extension)
        :return: the compare name (including the extension)
        """
        for photo in os.listdir(path):
            if os.path.splitext(photo)[0] == compare_name_short:
                return photo
        return ""

