import pygame as pg
from os import walk


def import_folder(path):
    surface_list = []
    paths = []

    for _, __, img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            paths.append(full_path)

        paths.sort(key=lambda x: x[-6:-4])
        for element in paths:
            image_surf = pg.image.load(element).convert_alpha()
            surface_list.append(image_surf)

    return surface_list

def loadSprite(imagePath, scale):
    newImage = pg.transform.scale(pg.image.load(imagePath),scale)
    return newImage

def drawButton(surface,xPos, yPos, width, height, text):    
    # Background
    pg.draw.rect(surface, (255,255,255), (xPos, yPos, width, height))
    
    # Button
    button = pg.draw.rect(surface, (0,0,0), (xPos + 5, yPos + 5, width - 10, height - 10))
    
    # Text
    surface.blit(text, (xPos + 18, yPos + 10))

    return button
