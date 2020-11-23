from factor import *
from factor_graph import *
from belief_propagation import *
from common_context import *

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
		self.context = common_context()
		self.tmp_factor_graph = None
		if self.skeleton is not None:
			self.horizon = len(self.skeleton)
			self.tmp_factor_graph = self.get_temporal_factor_graph(plan_skeleton)


	#not generalizable to other domains
	def get_precondition(self, action):
		preconditions=[]
		if action[0] == 'pick':
			preconditions.append(('observed', action[1]))
			preconditions.append(('hand-empty'))

		if action[0] == 'open':
			preconditions.append(('hand-empty'))

		if action[0] == 'fill-with':
			preconditions.append(('inhand', action[1]))

		if action[0] == 'stir':
			preconditions.append(('on', action[1], 'table'))
			preconditions.append(('hand-empty'))

		if action[0] == 'place':
			preconditions.append(('inhand', action[1]))

		return preconditions


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


	#not generalizable to other domains
	def get_action_for_goal(self, goal):
		if goal[0] == 'observed':
			target_object = goal[1]
			likely_location = self.search_for(target_object)
			return ('open', likely_location)

		elif goal[0] == 'inhand':
			return ('pick', goal[1])

		elif goal[0] == 'contains':
			return ('fill-with', goal[1], goal[2])

		elif goal[0] == 'is-stirred':
			return ('stir', goal[1])

		elif goal[0] == 'on':
			return ('place', goal[1], goal[2])

		else:
			return None 


	def search_for(self, target):
		belief_loc = self.context.context[target]
		places = [p[0] for p in belief_loc]
		prob_has = [pr[1] for pr in belief_loc]
		nearness = [self.context.nearness[p] for p in places]

		fg = factor_graph()
		for i in range(len(places)):
			fg.add_factor_node(places[i]+'_has_'+target, factor([places[i]], np.array([prob_has[i], 1-prob_has[i]])))

			fg.add_factor_node(places[i]+'_is_close', factor([places[i]], np.array([nearness[i], 1-nearness[i]])))
		fg.add_factor_node('are_consistent', factor(places, np.array([[[1,1],[1,1]],[[1,1],[1,1]]])))

		# plot_factor_graph(fg)
		
		bp = belief_propagation(fg)

		max_marg = 0
		max_place = places[0]
		for p in places:
			marg = bp.belief(p).get_distribution()[0]
			if marg > max_marg:
				max_marg = marg 
				max_place = p
		# print((max_place, max_marg))
		return max_place


	def plan(self):
		current_hl_node = self.tmp_factor_graph[self.time_step]
		for pre_condition in current_hl_node.pre_conditions:
			if pre_condition not in self.observation:
				return self.get_action_for_goal(pre_condition)
				
		self.time_step += 1
		if self.time_step == self.horizon:
			return 'Fin'
		return self.get_action_for_goal(current_hl_node.effect)




