import numpy as np 

class common_context:
	def __init__(self):
		self.context = \
			{
				'cup': [('dishes_drawer',0.3), ('spices_drawer',0.35), ('miscellaneous_drawer',0.3)],
				'large_cup': [('dishes_drawer',0.3), ('spices_drawer',0.35), ('miscellaneous_drawer',0.3)]
				#'coffee': [('dishes_drawer',0.3), ('spices_drawer',0.25), ('miscellaneous_drawer',0.25)],
				#'spices_drawer': [('dishes_drawer',0), ('spices_drawer',1), ('miscellaneous_drawer',0)]
			}
		self.nearness = {'dishes_drawer':0.3,
						 'spices_drawer':0.35,
						 'miscellaneous_drawer': 0.3
						 }