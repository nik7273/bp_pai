import numpy as np 

class common_context:
	def __init__(self, prob = None):
		self.context = \
			{
				'cup': [('dishes_drawer',prob[0][0][0]), ('spices_drawer',prob[0][0][1]), ('miscellaneous_drawer',prob[0][0][2])],
				'large_cup': [('dishes_drawer',prob[1][0][0]), ('spices_drawer',prob[1][0][1]), ('miscellaneous_drawer',prob[1][0][2])]
				#'coffee': [('dishes_drawer',0.3), ('spices_drawer',0.25), ('miscellaneous_drawer',0.25)],
				#'spices_drawer': [('dishes_drawer',0), ('spices_drawer',1), ('miscellaneous_drawer',0)]
			}
		self.nearness = {'dishes_drawer':0.3,
						 'spices_drawer':0.35,
						 'miscellaneous_drawer': 0.3
						 } # how close drawer is to robot's init pos