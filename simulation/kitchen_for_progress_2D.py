import os, sys
import pygame
import time
import math
import copy 

pygame.init()
pygame.display.set_caption('Kitchen For Progress 2D')


class utensil:
    def __init__(self, x, y, image_path,image_width,image_height,
                object_name,cx):
        self.x = x
        self.y = y
        self.dest = (self.x,self.y)
        self.cx = cx
        self.cy= 0
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
		self.win = pygame.display.set_mode((626,391))
		self.fps = 160
		time.sleep(15)
		self.gripper_width = 26
		self.prepend = '/home/bill/pai/bp_pai/simulation/'
		self.clock = pygame.time.Clock()
		self.initialize_items()
		self.refresh_window()


	def initialize_items(self):
		self.dishes_drawer = utensil(130,-10,self.prepend+'assets/dishes_drawer.png', 0,0,'dishes_drawer',0 )
		self.spices_drawer = utensil(190,-10,self.prepend+'assets/spices_drawer.png', 0,0,'dishes_drawer',0 )
		self.miscellaneous_drawer = utensil(250,-10,self.prepend+'assets/miscellaneous_drawer.png', 0,0,'dishes_drawer',0 )
		self.left_gripper = utensil(50,-150,self.prepend+'assets/left_gripper.png', 0,0,'dishes_drawer',0 )
		self.right_gripper = utensil(80,-150,self.prepend+'assets/right_gripper.png', 0,0,'dishes_drawer',0 )
		self.gripper_xy = [0, -100]
		self.mug = utensil(422,222,self.prepend+'assets/mug.png', 0,0,'mug',0 )
		self.stirrer = utensil(446,212,self.prepend+'assets/stirrer.png', 0,0,'stirrer',0 )
		self.coffee = utensil(477,222,self.prepend+'assets/coffee.png', 0,0,'coffee',0 )	
		self.tap = utensil(32,142,self.prepend+'assets/tap.png', 0,0,'tap',0 )

		self.items = {'dishes_drawer':self.dishes_drawer, 'spices_drawer':self.spices_drawer,'miscellaneous_drawer':self.miscellaneous_drawer,'left_gripper':self.left_gripper, 'right_gripper':self.right_gripper,'cup':self.mug, 'coffee':self.coffee, 'stirrer':self.stirrer}

		self.initialize_grasp_configs()


	def initialize_grasp_configs(self):
		self.dishes_drawer.cx = 145
		self.dishes_drawer.cy = -50 
		self.dishes_drawer.width = 20

		self.spices_drawer.cx = 205
		self.spices_drawer.cy = -50 
		self.spices_drawer.width = 20

		self.miscellaneous_drawer.cx = 265
		self.miscellaneous_drawer.cy = -50 
		self.miscellaneous_drawer.width = 20

		self.mug.cx = 145
		self.mug.cy = 10 
		self.mug.width = 23

		self.stirrer.cx = 170
		self.stirrer.cy = -15 
		self.stirrer.width = 10

		self.coffee.cx = 202
		self.coffee.cy = 10 
		self.coffee.width = 26

		self.tap_fill = (-185, 10)


	
	def update_gripper(self, width=30):
		self.gripper_width=width
		x = self.gripper_xy[0]
		y = self.gripper_xy[1]
		self.win.blit(self.left_gripper.body, (x,y))
		self.win.blit(self.right_gripper.body, (x+self.gripper_width,y))

		
	def display_items(self):
		self.win.blit(self.dishes_drawer.body, (self.dishes_drawer.x, self.dishes_drawer.y))
		self.win.blit(self.spices_drawer.body, (self.spices_drawer.x,self.spices_drawer.y))
		self.win.blit(self.miscellaneous_drawer.body, (self.miscellaneous_drawer.x,self.miscellaneous_drawer.y))
		self.win.blit(self.mug.body, (self.mug.x,self.mug.y))
		self.win.blit(self.stirrer.body, (self.stirrer.x,self.stirrer.y))
		self.win.blit(self.coffee.body, (self.coffee.x,self.coffee.y))
		self.win.blit(self.tap.body, (self.tap.x,self.tap.y))
		# self.gripper_xy = (-185, 10)
		self.update_gripper(self.gripper_width)


	def refresh_window(self):
		self.win.blit(pygame.image.load(self.prepend+'assets/kitchen.jpg'),(0,0))
		self.display_items()
		pygame.display.update()
		self.clock.tick(self.fps)

	def pick_motion(self, itemname):
		item = self.items[itemname]
		orig_x = self.gripper_xy[0]
		orig_y = self.gripper_xy[1]

		while math.fabs(item.cx - self.gripper_xy[0]) > 0:
			if item.cx - self.gripper_xy[0] > 0:
				self.gripper_xy[0] += 1
			elif item.cx - self.gripper_xy[0] < 0:
				self.gripper_xy[0] -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(item.cy - self.gripper_xy[1]) > 0:
			if item.cy - self.gripper_xy[1] > 0:
				self.gripper_xy[1] +=1 
			elif item.cy - self.gripper_xy[1] < 0:
				self.gripper_xy[1] -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		#retracting
		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_y - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()


	def place_on_table(self, itemname):
		item = self.items[itemname]
		ox = 0
		oy = -100
		orig_x = item.cx - 200
		orig_y = item.cy

		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_x - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

			#retracting
		while math.fabs(oy - self.gripper_xy[1]) > 0:
			if oy - self.gripper_xy[1] > 0:
				self.gripper_xy[1] +=1 
			elif oy - self.gripper_xy[1] < 0:
				self.gripper_xy[1] -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(ox - self.gripper_xy[0]) > 0:
			if ox - self.gripper_xy[0] > 0:
				self.gripper_xy[0] += 1
			elif ox - self.gripper_xy[0] < 0:
				self.gripper_xy[0] -=1
			self.update_gripper(item.width)
			self.refresh_window()


	def open_drawer(self, drawer_name):
		self.pick_motion(drawer_name)
		item = self.items[drawer_name]
		orig_x = item.cx
		orig_y = item.cy
		ox = 0
		oy = -100
		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_x - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		#retracting
		while math.fabs(oy - self.gripper_xy[1]) > 0:
			if oy - self.gripper_xy[1] > 0:
				self.gripper_xy[1] +=1 
			elif oy - self.gripper_xy[1] < 0:
				self.gripper_xy[1] -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(ox - self.gripper_xy[0]) > 0:
			if ox - self.gripper_xy[0] > 0:
				self.gripper_xy[0] += 1
			elif ox - self.gripper_xy[0] < 0:
				self.gripper_xy[0] -=1
			self.update_gripper(item.width)
			self.refresh_window() 

	def fill_with_water(self, itemname):
		item = self.items[itemname]
		orig_x = self.gripper_xy[0]
		orig_y = self.gripper_xy[1]
		ox = self.tap_fill[0]
		oy = self.tap_fill[1]

		while math.fabs(oy - self.gripper_xy[1]) > 0:
			if (oy - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (oy - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(ox - self.gripper_xy[0]) > 0:
			if (ox - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (ox - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()	
# filling
		time.sleep(3)
		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_x - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()


	def rotate_center(self, image, angle):
		rotated_image = pygame.transform.rotate(image, angle)
		new_rect = rotated_image.get_rect(center = image.get_rect().center)
		return rotated_image, new_rect


	def fill_cup_with_coffee(self):
		itemt = self.items['cup']
		ox = 0
		oy = -100
		orig_x = itemt.cx - 200
		orig_y = itemt.cy-50
		item = self.items['coffee']

		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_x - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		# orig_body = copy.deepcopy(item.body)
		item.body,_ = self.rotate_center(item.body, 90)
		self.refresh_window()
		time.sleep(2)
		item.body,_ = self.rotate_center(item.body, -90)
		self.refresh_window()
		time.sleep(1)

		#retracting
		while math.fabs(oy - self.gripper_xy[1]) > 0:
			if oy - self.gripper_xy[1] > 0:
				self.gripper_xy[1] +=1 
				item.y +=1
			elif oy - self.gripper_xy[1] < 0:
				self.gripper_xy[1] -= 1
				item.y -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(ox - self.gripper_xy[0]) > 0:
			if ox - self.gripper_xy[0] > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif ox - self.gripper_xy[0] < 0:
				self.gripper_xy[0] -=1
				item.x +=1
			self.update_gripper(item.width)
			self.refresh_window() 


	def stir(self, itemname):
		self.pick_motion('stirrer')

		itemt = self.items['cup']
		ox = 0
		oy = -100
		orig_x = itemt.cx - 200
		orig_y = itemt.cy-30
		item = self.items['stirrer']

		while math.fabs(orig_x - self.gripper_xy[0]) > 0:
			if (orig_x - self.gripper_xy[0]) > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif (orig_x - self.gripper_xy[0]) < 0:
				self.gripper_xy[0] -= 1
				item.x -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(orig_y - self.gripper_xy[1]) > 0:
			if (orig_y - self.gripper_xy[1]) > 0:
				self.gripper_xy[1]+=1
				item.y += 1
			elif (orig_y - self.gripper_xy[1]) < 0:
				self.gripper_xy[1]-=1
				item.y -= 1
			self.update_gripper(item.width)
			self.refresh_window()

		time.sleep(0.25)
		self.gripper_xy[0]+=10
		item.x+=10
		self.update_gripper(item.width)
		self.refresh_window()
		time.sleep(0.25)
		self.gripper_xy[0]-=10
		item.x-=10
		self.update_gripper(item.width)
		self.refresh_window()

		#retracting
		while math.fabs(oy - self.gripper_xy[1]) > 0:
			if oy - self.gripper_xy[1] > 0:
				self.gripper_xy[1] +=1 
				item.y +=1
			elif oy - self.gripper_xy[1] < 0:
				self.gripper_xy[1] -= 1
				item.y -=1
			self.update_gripper(item.width)
			self.refresh_window()

		while math.fabs(ox - self.gripper_xy[0]) > 0:
			if ox - self.gripper_xy[0] > 0:
				self.gripper_xy[0] += 1
				item.x +=1
			elif ox - self.gripper_xy[0] < 0:
				self.gripper_xy[0] -=1
				item.x +=1
			self.update_gripper(item.width)
			self.refresh_window() 


	
	def parse_and_execute(self, action):
		if action[0] == 'open':
			self.open_drawer(action[1])
		elif action[0] == 'pick':
			self.pick_motion(action[1])
		elif action[0] == 'fill-with':
			if action[2] == 'water':
				self.fill_with_water(action[1])
			elif action[2] == 'coffee':
				self.fill_cup_with_coffee()
		elif action[0] == 'drop-on-table':
			self.place_on_table(action[1])
		elif action[0] == 'stir':
			self.stir(action[1])



if __name__ == '__main__':
	env = environment()
	env.refresh_window()
	env.pick_motion('cup')
	env.place_on_table('cup')
	# env.pick_motion('coffee')
	# env.fill_cup_with_coffee()
	env.stir('cup')
	# env.open_drawer('miscellaneous_drawer')
	# env.place_on_table('coffee')
	# env.pick_motion('cup')
	# env.fill_with_water('cup')
	while True:
		env.refresh_window()