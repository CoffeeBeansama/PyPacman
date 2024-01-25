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
