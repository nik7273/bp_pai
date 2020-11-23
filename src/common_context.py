import numpy as np 

class common_context:
	def __init__(self):
		self.context = \
			{'cup':   [('dishes_drawer',0.35), ('spices_drawer',0.3), ('miscellaneous_drawer',0.35)],
			'coffee': [('dishes_drawer',0.3), ('spices_drawer',0.4), ('miscellaneous_drawer',0.3)]
			}
		self.nearness = {'dishes_drawer':0.35,
						 'spices_drawer':0.3,
						 'miscellaneous_drawer':0.35
						 }