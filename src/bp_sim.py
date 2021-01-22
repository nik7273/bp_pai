import kitchen2d.kitchen_stuff as ks
from kitchen2d.kitchen_stuff import Kitchen2D
from kitchen2d.gripper import Gripper
import numpy as np
import time
from copy import copy

SETTING = {
    'do_gui': False,
    'sink_w': 10.,
    'sink_h': 5.,
    'sink_d': 1.,
    'sink_pos_x': 20.,
    'left_table_width': 50.,
    'right_table_width': 50.,
    'faucet_h': 12.,
    'faucet_w': 5.,
    'faucet_d': 0.5,
    'planning': False,
    'overclock': 50 # number of frames to skip when showing graphics.
}

def query_gui(action_type, kitchen):
    choice = input('Show GUI for {}? [y/n]'.format(action_type))
    if choice == 'y':
        print('Enabling GUI...')
        kitchen.enable_gui()
    else:
        print('Disabling GUI...')
        kitchen.disable_gui()

class item:
    def __init__(self):
        self.location = None
        self.in_gripper = False
        self.observable = False
        self.is_stirred = False
        self.is_poured = False
        self.contains = []
        #self.is_cooked = False

class BPSim:
    """
    Abstraction of Kitchen2D simulation to fit symbolic planning via BP Planner.
    """
    def __init__(self, gripper_init_pos=(20,40), gripper_init_angle=0):
        """
        Input(s):
            gripper_init_pos: (int, int),
            gripper_init_angle: int
        """
        self.kitchen = Kitchen2D(**SETTING)
        self.gripper = Gripper(self.kitchen, gripper_init_pos, gripper_init_angle)
        self.symbol_to_obj = {}
        self.cup = item()
        self.coffee = item()
        self.cup.location = 'dishes_drawer'
        self.coffee.location = 'spices_drawer'
        self.items = {'cup':self.cup, 'coffee':self.coffee}

    def move_drawer(self, drawer_sym, drop_pos=(-10, 10)):
        """
        Move `drawer_sym` out of the way and drop it at `drop_pos`.
        """
        query_gui('MOVE_DRAWER', self.kitchen)
        grasp = 0.306249162768 # tunable parameter for path planner
        drawer_obj = self.symbol_to_obj[drawer_sym]
        drawer_pos = drawer_obj.position

        self.gripper.find_path((drawer_pos[0], drawer_pos[1] + 10), 0)
        self.gripper.grasp(drawer_obj, grasp)

        self.gripper.find_path((drop_pos[0], drop_pos[1] + 10), 0)
        self.gripper.place(drop_pos, 0)

    def pick_up(self, obj_sym):
        """
        Pick up object represented by `obj_sym` in simulation.
        """
        query_gui('PICK_UP', self.kitchen)
        grasp = 0.306249162768 # tunable parameter for path planner
        obj = self.symbol_to_obj[obj_sym]
        obj_pos = obj.position
        self.gripper.find_path((obj_pos[0], obj_pos[1] + 10), 0)
        self.gripper.grasp(obj, grasp)

    def place(self, pos):
        """
        Place held object at position `pos`.
        """
        query_gui('PLACE', self.kitchen)
        self.gripper.place(pos, 0)

    def fill(self, duration=1):
        """
        Fill held object with water for `duration` seconds
        """
        query_gui('FILL', self.kitchen)
        self.gripper.get_liquid_from_faucet(duration)

    def pour(self, obj_sym):
        """
        Pour liquid into object represented by `obj_sym`.
        """
        query_gui('POUR', self.kitchen)
        grasp = 0.306249162768
        rel_x = 3.70183788428
        rel_y = 9.01263886707
        dangle = 1.59620914618
        dangle *= np.sign(rel_x)
        obj = self.symbol_to_obj[obj_sym]
        print(self.gripper.pour(obj, (rel_x, rel_y), dangle))
        # After every pour, place the object
        self.gripper.place((obj.position[0]+ obj.usr_w + 1, 0), 0)

    def scoop(self, obj_sym, spoon_sym, dump_sym, spoon_grasp_pos=(23, 10), drop_pos=(0,10)):
        """
        Grasp `spoon_sym`, scoop from `obj_sym`, dump contents into `dump_sym`.
        """
        query_gui('SCOOP', self.kitchen)
        # Tunable parameters received from the active sampling method
        rel_x1 = 0.0276296492162
        rel_y1 = 0.611922721287
        rel_x2 = 0.846900041891
        rel_y2 = 0.056968220054
        rel_x3 = 0.960750333945
        rel_y3 = 0.126499043204
        grasp = 0.883195866437
        rel_pos1 = (rel_x1, rel_y1); rel_pos2 = (rel_x2, rel_y2); rel_pos3 = (rel_x3, rel_y3)

        spoon = self.symbol_to_obj[spoon_sym]
        obj = self.symbol_to_obj[obj_sym]
        dump = self.symbol_to_obj[dump_sym]

        self.gripper.set_grasped(spoon, grasp, spoon_grasp_pos, 0)
        print(self.gripper.scoop(obj, rel_pos1, rel_pos2, rel_pos3))

        # Dumping contents of scoop
        self.gripper.dump(dump, 0.9) # 0.9 is tunable

        # Placing spoon
        self.gripper.place(drop_pos, 0)

    def stir(self, stir_sym, obj_sym, stir_grasp_pos=(10,10), num_stirs=5):
        """
        Pick up `stir_sym` and stir in `obj_sym`.
        `stir_grasp_pos`: position of gripper after picking up stirrer
        `num_stirs`: number of times to stir inside `obj_sym`
        """
        query_gui('STIR', self.kitchen)        
        stirrer = self.symbol_to_obj[stir_sym]
        obj = self.symbol_to_obj[obj_sym]
        
        self.gripper.set_grasped(stirrer, 0.8, stir_grasp_pos, 0)
        self.gripper.stir(obj, (0, 0.0), (1, 0.0), num_stirs=num_stirs)
        self.gripper.find_path(self.gripper.position + [0, 5], 0)

    def init_mapping(self, registry):
        """
        Creates mapping of symbol to object.
        """
        self.symbol_to_obj = copy(registry)

    def parse_and_execute(self, action):
        """
        Execute corresponding action in environment.
        Input(s):
            - action: (action_name, object_name, ...) depending on action
        """
        if action[0] == 'open':
            if len(action) > 2:
                self.move_drawer(action[1], drop_pos=action[2])
            else:
                self.move_drawer(action[1])
            for item in self.items:
                if self.items[item].location == action[1]:
                        self.items[item].observable = True
                     
        elif action[0] == 'pick':
            self.pick_up(action[1])
            self.items[action[1]].in_gripper = True

        elif action[0] == 'fill':
            # action[1] will contain the correct cup, but k2d doesn't need it
            self.fill()
            self.items[action[1]].contains.append('water')

        elif action[0] == 'place':
            self.place(action[1])
            self.items[action[1]].location = action[2]
            self.items[action[1]].in_gripper = False

        elif action[0] == 'stir':
            if len(action) > 2:
                self.stir(action[0], action[1], stir_grasp_pos=action[2])
            else:
                self.stir(action[0], action[1])
            self.items[action[1]].is_stirred = True 

        elif action[0] == 'scoop':
            self.scoop()

        elif action[0] == 'pour':
            # Sloppy parameter checking; in particular fails when spoon_grasp_pos not included and drop_pos is
            if len(action) == 3:
                self.pour(action[0], action[1], action[2])
            elif len(action) == 4:
                self.pour(action[0], action[1], action[2], spoon_grasp_pos=action[3])
            elif len(action) == 5:
                self.pour(action[0], action[1], action[2], spoon_grasp_pos=action[3], drop_pos=action[4])

    def get_observation_tuple(self):
        """
        Grabs observations from environment for planner.
        """
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
            #if it.is_cooked:
            #	observation.append(('is-cooked', item))
            if 'drawer' != it.location[-6:]:
                observation.append(('on', item, it.location))
        if hand_empty:
            observation.append(('hand-empty'))
        return observation


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

    cup1_x = -20
    cup2_x = 0
    large_cup_x = 10

    # Create objects
    drawer1 = ks.make_drawer(bp_sim.kitchen, (cup1_x, pour_from_h+2), 0, pour_from_w*2 + 2.5*holder_d, pour_from_h, holder_d)
    cup1 = ks.make_cup(bp_sim.kitchen, (cup1_x,0), 0, pour_from_w, pour_from_h, holder_d)
    drawer2 = ks.make_drawer(bp_sim.kitchen, (cup2_x, pour_from_h+2), 0, pour_from_w*2 + 2.5*holder_d, pour_from_h, holder_d)
    cup2 = ks.make_cup(bp_sim.kitchen, (cup2_x,0), 0, pour_to_w, pour_to_h, holder_d)
    large_cup = ks.make_cup(bp_sim.kitchen, (large_cup_x, 0), 0, scoop_w, scoop_h, holder_d)

    return drawer1, cup1, drawer2, cup2, large_cup

# def main():
#     bp_sim = BPSim()

#     # Example 
#     sym_list = ['drawer1', 'cup1', 'drawer2', 'cup2', 'large_cup']
#     obj_list = build_world(bp_sim)
#     bp_sim.init_mapping(dict(zip(sym_list, obj_list)))

#     # Actions
#     bp_sim.move_drawer('drawer1')
#     bp_sim.pick_up('cup1')
#     bp_sim.fill(1)
#     query_gui('PAUSE', bp_sim.kitchen)

# if __name__ == '__main__':
#     main()
