import matplotlib.pyplot as plt
from os import path, mkdir
from PIL import Image
import json


class barChart:
    def __init__(self):
        with open("data.json", "r") as jsonFile:
            data = json.load(jsonFile)
        self.marks = []
        self.subjects = []
        self.title = ""
        self.y_axis_range = [0, data["max"]]

        if not path.isdir(".\\charts"):
            mkdir(".\\charts")

    def generate(self, marks, subjects, name, title="Test"):

        plt.ylim(self.y_axis_range)
        print(name)
        details = dict(zip(subjects, marks))
        print(details)
        plt.bar(
            subjects,
            marks,
            width=0.72,
            color=["orange", "limegreen", "violet", "gold", "royalblue"],
        )
        plt.xlabel("Subjects")
        plt.ylabel("Marks")
        plt.xticks(subjects)
        plt.title(title)
        plt.savefig(f"charts\\{name}.jpg")
        self.compress(f"charts\\{name}.jpg", name)
        plt.clf()

    def compress(self, chartPath, name):
        n = 0.6
        image = Image.open(chartPath)
        [imageSizeWidth, imageSizeHeight] = image.size
        newImageSizeWidth = int(imageSizeWidth * n)
        newImageSizeHeight = int(imageSizeHeight * n)

        image = image.resize((newImageSizeWidth, newImageSizeHeight), Image.ANTIALIAS)
        image.save(f"charts\\ppm\\{name}.ppm", "ppm")

