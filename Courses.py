from PIL import Image, ImageFont, ImageDraw
from PyQt5.QtWidgets import QFileDialog


class Courses:
    def __init__(self, name, rab, data):
        self.name = name
        self.rab = rab
        self.data = data
        self.work(self.name, self.rab, self.data)

    def work(self, name, rab, data):
        img = Image.open('certificates/courses.jpg')
        font = ImageFont.truetype("CENTURY.TTF", 32)
        font1 = ImageFont.truetype("CENTURY.TTF", 12)
        draw = ImageDraw.Draw(img)
        draw.text((250, 276), f'{name}', (0, 0, 0), font=font)
        draw.text((360, 366), f'{rab}', (0, 0, 0), font=font)
        draw.text((700, 581), f"{data}", (0, 0, 0), font=font1)
        dirlist = QFileDialog.getExistingDirectory()
        img.save(f'{dirlist}/Courses.jpg')
