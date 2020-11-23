import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *
from factor_graph import *
from belief_propagation import *
from bp_planning import *
from world import *

# planner = bp_pai()
# planner.search_for('cup')
ewiase = World()
ewiase.state_transition(('open','dishes_drawer'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('pick','cup'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('fill-with','cup','water'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('place','cup','table'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('open','spices_drawer'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('pick','coffee'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('fill-with','cup','coffee'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('place','coffee','table'))
print(ewiase.get_observation_tuple())
print(' ')
ewiase.state_transition(('stir','cup'))
print(ewiase.get_observation_tuple())
print(' ')