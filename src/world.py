import numpy as np 

class item:
	def __init__(self):
		self.location = None
		self.in_gripper = False
		self.observable = False
		self.is_stirred = False
		self.is_cooked = False
		self.contains = []

class World:
	def __init__(self):
		self.cup = item()
		self.coffee = item()
		self.cup.location = 'dishes_drawer'
		self.coffee.location = 'spices_drawer'
		self.items = {'cup':self.cup, 
					  'coffee':self.coffee}


	def get_observation_tuple(self):
		observation = []
		hand_empty = True

		for item in self.items:
			it = self.items[item]

			if it.in_gripper:
				observation.append(('inhand',item))
				hand_empty = False
			for content in it.contains:
				observation.append(('contains', item, content))
			if it.observable:
				observation.append(('observed', item))
			if it.is_stirred:
				observation.append(('is-stirred', item))
			if it.is_cooked:
				observation.append(('is-cooked', item))
			if 'drawer' != it.location[-6:]:
				observation.append(('on', item, it.location))
		if hand_empty:
			observation.append(('hand-empty'))
		return observation


	def state_transition(self, action):
		if action[0] == 'pick':
			self.items[action[1]].in_gripper = True

		elif action[0] == 'fill-with':
			self.items[action[1]].contains.append(action[2])

		elif action[0] == 'stir':
			self.items[action[1]].is_stirred = True 
			self.items[action[1]].is_cooked  = True 

		elif action[0] == 'open':
			for item in self.items:
				if self.items[item].location == action[1]:
					 self.items[item].observable = True

		elif action[0] == 'place':
			self.items[action[1]].location = action[2]
			self.items[action[1]].in_gripper = False

		# return 