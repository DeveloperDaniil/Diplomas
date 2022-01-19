from PIL import Image, ImageDraw, ImageFont
from PyQt5.QtWidgets import QFileDialog


class Participant:
    def __init__(self, name, date):
        self.name = name
        self.date = date
        self.work(self.name, self.date)

    def work(self, name, date):
        img = Image.open('certificates/participant.jpg')
        font = ImageFont.truetype("CENTURY.TTF", 32)
        font1 = ImageFont.truetype("CENTURY.TTF", 16)
        draw = ImageDraw.Draw(img)
        draw.text((170, 220), f'{name}', (0, 0, 0), font=font)
        draw.text((177, 425), f"{date}", (0, 0, 0), font=font1)
        dirlist = QFileDialog.getExistingDirectory()
        img.save(f'{dirlist}/Participant.jpg')
