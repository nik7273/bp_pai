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
		self.holding = 'cup'
		self.previously_opened = []
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
			preconditions.append(('hand-empty'))
			preconditions.append(('observed', action[1]))
			
		if action[0] == 'open':
			preconditions.append(('hand-empty'))

		if action[0] == 'fill':
			preconditions.append(('inhand', action[1]))

		if action[0] == 'stir':
			preconditions.append(('on', action[1], 'table'))
			preconditions.append(('hand-empty'))

		if action[0] == 'place':
			preconditions.append(('inhand', action[1]))

		return preconditions


	def get_effect(self, action):
		effects=[]
		if action[0] == 'pick':
			effects.append(('inhand', action[1]))

		elif action[0] == 'open':
			pass

		elif action[0] == 'fill':
			effects.append(('contains', action[1], 'water'))#action[2]))
			# effects.append(('contains', action[1], action[2]))
			effects.append(('inhand', action[1]))

		elif action[0] == 'stir':
			effects.append(('is-stirred', action[1]))

		elif action[0] == 'place':
			effects.append(('on', action[1], action[2]))
			effects.append(('hand-empty'))
		return effects


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
			likely_location = self.search_for(target_object,red=self.previously_opened)
			self.previously_opened.append(likely_location)
			return ('open', likely_location)

		elif goal[0] == 'inhand':
			self.holding = goal[1]
			return ('pick', goal[1])

		elif goal[0] == 'contains':
			return ('fill', goal[1])#, goal[2])

		elif goal[0] == 'is-stirred':
			return ('stir', goal[1])

		elif goal[0] == 'on':
			return ('place', goal[1], goal[2])

		elif goal == 'hand-empty':
			# 'place' parameter is `pos` tuple (x,y)
			return ('place', self.holding, 'place_to_default')#self.default_pos) # placing where? want a deterministic location?

		else:
			print(goal)
			return None 


	def search_for(self, target,red=[]):
		belief_loc = self.context.context[target]
		places = [p[0] for p in belief_loc]
		prob_has = [pr[1] for pr in belief_loc]
		if len(red)>0:
			for r in red:
				ind = places.index(r)
				prob_has[ind] = 0
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
		if self.time_step == self.horizon:
			return 'Fin'
		current_hl_node = self.tmp_factor_graph[self.time_step]
		for pre_condition in current_hl_node.pre_conditions:
			if pre_condition not in self.observation:
				# print('not satisfied: ',pre_condition)
				return self.get_action_for_goal(pre_condition)
				
		self.time_step += 1
		# print('time_step: ',self.time_step)
		self.previously_opened=[]
		return self.get_action_for_goal(current_hl_node.effect[0])




