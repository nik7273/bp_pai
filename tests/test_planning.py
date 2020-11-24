import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
os.sys.path.append(os.path.realpath(script_path + '/../simulation/'))
from factor import *
from factor_graph import *
from belief_propagation import *
from bp_planning import *
from world import *
from kitchen_for_progress_2D import *
# planner = bp_pai()
# planner.search_for('cup')
# ewiase = World()
# ewiase.state_transition(('open','dishes_drawer'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('pick','cup'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('fill-with','cup','water'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('place','cup','table'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('open','spices_drawer'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('pick','coffee'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('fill-with','cup','coffee'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('place','coffee','table'))
# print(ewiase.get_observation_tuple())
# print(' ')
# ewiase.state_transition(('stir','cup'))
# print(ewiase.get_observation_tuple())
# print(' ')
skeleton = [('pick','cup'), ('fill-with', 'cup', 'water'), ('pick', 'coffee'), ('fill-with', 'cup', 'coffee'), ('stir','cup')]
terminate = False
ewiase = World()
planner = bp_pai(init_observation = ewiase.get_observation_tuple(),
				 plan_skeleton = skeleton)
env = environment()
# planner.search_for('cup')
timestep = 0
while not terminate:
	action = planner.plan()
	print(str(timestep)+': ', action)
	if action == 'Fin':
		terminate = True
	else:
		ewiase.state_transition(action)
		env.parse_and_execute(action)
		observation = ewiase.get_observation_tuple()
		planner.update_belief(observation)

	timestep += 1
	if timestep > 100:
		break