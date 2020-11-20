import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *
from factor_graph import *
from belief_propagation import *

pgm_1 = factor_graph()
# pgm_1.add_factor_node('cereal', factor(['has_cup', 'is_close']))

pgm_1.add_factor_node('cereal_has_cup', factor(['cereal']))
pgm_1.add_factor_node('cereal_is_close', factor(['cereal']))
pgm_1.add_factor_node('dishes_has_cup', factor(['dishes']))
pgm_1.add_factor_node('dishes_is_close', factor(['dishes']))
pgm_1.add_factor_node('spices_has_cup', factor(['spices']))
pgm_1.add_factor_node('spices_is_close', factor(['spices']))
pgm_1.add_factor_node('are_feasible', factor(['cereal', 'dishes', 'spices']))

cereal_has_cup = factor(['cereal'], np.array([0.4,0.5]))
dishes_has_cup = factor(['dishes'], np.array([0.7,0.3]))
spices_has_cup = factor(['spices'], np.array([0.4,0.6]))

cereal_is_close = factor(['cereal'], np.array([0.5,0.5]))
dishes_is_close = factor(['dishes'], np.array([0.3,0.7]))
spices_is_close = factor(['spices'], np.array([0.17,0.1]))

are_feasible = factor(['cereal','dishes','spices'], np.array([[[1,1],[1,1]],[[1,1],[1,1]]]))

 

pgm_1.change_factor_distribution('cereal_has_cup',cereal_has_cup)
pgm_1.change_factor_distribution('dishes_has_cup',dishes_has_cup)
pgm_1.change_factor_distribution('spices_has_cup',spices_has_cup)
pgm_1.change_factor_distribution('cereal_is_close',cereal_is_close)
pgm_1.change_factor_distribution('dishes_is_close',dishes_is_close)
pgm_1.change_factor_distribution('spices_is_close',spices_is_close)

pgm_1.change_factor_distribution('are_feasible',are_feasible)

bp = belief_propagation(pgm_1)
print('cereal', bp.belief('cereal').get_distribution())
print('dishes', bp.belief('dishes').get_distribution())
print('spices', bp.belief('spices').get_distribution())
plot_factor_graph(pgm_1)