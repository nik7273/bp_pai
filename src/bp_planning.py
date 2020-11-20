from factor import *
from factor_graph import *
from belief_propagation import *

class Temporal_node:
	def __init__(self):
		self.pre_conditions=None
		self.effect = None
		self.transition_to_next = False
		self.active = False


class bp_pai:
	def __init__(self, init_observation=None, plan_skeleton=None, goal = None):
		self.skeleton = plan_skeleton
		self.goal = goal
		self.time_step = 0
		self.horizon = 0
		self.observation = init_observation
		self.tmp_factor_graph = None
		if self.skeleton is not None:
			self.horizon = len(self.skeleton)
			self.tmp_factor_graph = self.get_temporal_factor_graph(plan_skeleton)


	def get_temporal_factor_graph(self, skeleton):
		tmp_fg = []
		for action in skeleton:
			pre_condition = self.get_precondition(action)
			effect = self.get_effect(action)
			tmp_node = Temporal_node()
			tmp_node.pre_conditions=pre_condition
			tmp_node.effect=effect
			tmp_fg.append(tmp_node)
		return tmp_fg


	def update_belief(self, observation):
		self.observation = observation 


	def plan(self):
		current_hl_node = self.tmp_factor_graph[self.time_step]
		for pre_condition in current_hl_node.pre_conditions:
			if pre_condition not in self.observation:
				yield self.get_action_for_goal(pre_condition)
				
		self.time_step += 1
		return self.get_action_for_goal(current_hl_node.effect)


	def get_action_for_goal(self, goal):
		if goal[0] == 'observed':
			target_object = goal[1]
			likely_location = self.search_for(target_object)
			return ('open', likely_location)

		elif goal[0] == 'inhand':
			return ('pick', goal[1])

		elif goal[0] == 'contains':
			return ('fill-with', goal[1], goal[2])

		else:
			return None 


	def search_for(self, target):
		


