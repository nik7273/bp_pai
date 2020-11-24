import os, sys
import pygame
import time

pygame.init()
pygame.display.set_caption('Kitchen For Progress 2D')


class utensil:
    def __init__(self, x, y, image_path,image_width,image_height,
                object_name,cx):
        self.x = x
        self.y = y
        self.cx = cx
        self.cy= 480-image_height
        self.width = image_width
        self.height = image_height
        self.body = pygame.image.load(image_path)
        self.item_at_left = None
        self.item_at_right = None
        self.item_on_top = None
        self.item_on_bottom = None
        self.on_table = False
        self.on_clutter_or_table = False
        self.onsomething = False
        self.being_held = False
        self.name = object_name
        self.holding = None #only for gripper


class environment:
	def __init__(self):
		