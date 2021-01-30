import sys
import os
import time
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
os.sys.path.append(os.path.realpath(script_path + '/../simulation/'))
from factor import *
from factor_graph import *
from belief_propagation import *
from bp_planning import *
from world import *
from kitchen_for_progress_2D import *
from bp_sim import *

def build_world(bp_sim):
    """
    Returns tuple of objects in world.
    """
    # Preset parameters that make this effective
    pour_to_w = 4.17393549546
    pour_to_h = 4.05998671658
    pour_from_w = 3.61443970857
    pour_from_h = 4.51052132521

    scoop_w = 5.388370713
    scoop_h = 4.52898336641
    holder_d = 0.5

    bp_sim.default_pos = (40, 10)

    cup1_x = -20
    cup2_x = 0
    large_cup_x = 10

    # Create objects
    drawer1 = ks.make_drawer(bp_sim.kitchen, (cup1_x, pour_from_h+2), 0, pour_from_w*2 + 2.5*holder_d, pour_from_h+2, holder_d)
    cup1 = ks.make_cup(bp_sim.kitchen, (cup1_x,0), 0, pour_from_w, pour_from_h, holder_d)
    drawer2 = ks.make_drawer(bp_sim.kitchen, (cup2_x, pour_from_h+2), 0, pour_from_w*2 + 2.5*holder_d, pour_from_h+2, holder_d)
    cup2 = ks.make_cup(bp_sim.kitchen, (cup2_x,0), 0, pour_to_w, pour_to_h, holder_d)
    drawer3 = ks.make_drawer(bp_sim.kitchen, (large_cup_x, pour_from_h+2), 0, pour_from_w*2 + 2.5*holder_d, pour_from_h+2, holder_d)
    large_cup = ks.make_cup(bp_sim.kitchen, (large_cup_x, 10), 0, scoop_w, scoop_h, holder_d)

    return drawer1, cup1, drawer2, cup2, drawer3, large_cup

skeleton = [('pick','cup'), ('fill', 'cup'), ('pick', 'large_cup')]
bp_sim = BPSim()
sym_list = ['dishes_drawer', 'cup', 'spices_drawer', 'cup2', 'miscellaneous_drawer', 'large_cup']
obj_list = build_world(bp_sim)
bp_sim.init_mapping(dict(zip(sym_list, obj_list)))

planner = bp_pai(init_observation = bp_sim.get_observation_tuple(),
				 plan_skeleton = skeleton)

timestep = 0
terminate = False
while not terminate:
    action = planner.plan()
    print(str(timestep)+': ', action)
    if action == 'Fin':
        terminate = True
    else:
        bp_sim.parse_and_execute(action)
        observation = bp_sim.get_observation_tuple()
        planner.update_belief(observation)

    timestep += 1
    if timestep > 100:
        break