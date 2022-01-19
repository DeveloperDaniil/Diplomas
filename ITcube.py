from PIL import Image, ImageFont, ImageDraw
from PyQt5.QtWidgets import QFileDialog


class ITcube:
    def __init__(self, step, type, name, nom, ruk):
        self.step = step
        self.type = type
        self.name = name
        self.nom = nom
        self.ruk = ruk
        self.work(self.step, self.type, self.name, self.nom, self.ruk)

    def work(self, step, type, name, nom, ruk):
        img = Image.open('certificates/it_cub.jpg')
        font = ImageFont.truetype("CENTURY.TTF", 32)
        font1 = ImageFont.truetype("CENTURY.TTF", 16)
        font2 = ImageFont.truetype("CENTURY.TTF", 28)
        font3 = ImageFont.truetype("CENTURY.TTF", 16)
        font4 = ImageFont.truetype("CENTURY.TTF", 16)
        draw = ImageDraw.Draw(img)
        draw.text((190, 290), f'{step}', (255, 255, 255), font=font)
        draw.text((127, 325), f"{type}", (255, 255, 255), font=font1)
        draw.text((70, 350), f'<<{name}>>', (255, 255, 255), font=font2)
        draw.text((100, 385), f'Номинация <<{nom}>>', (255, 255, 255), font=font3)
        draw.text((260, 500), f'{ruk}', (255, 255, 255), font=font4)
        dirlist = QFileDialog.getExistingDirectory()
        img.save(f'{dirlist}/ITcube.jpg')
