import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *
from factor_graph import *

pgm_1 = factor_graph()
pgm_1.add_factor_node('p1', factor(['x1', 'x2', 'x3']))
pgm_1.add_factor_node('p2', factor(['x2', 'x4'])) 

pgm_2 = string2factor_graph('phi_1(a,b,c)phi_2(b,c,d,e)psi_3(e,c)psi_4(d)') 

plot_factor_graph(pgm_2)