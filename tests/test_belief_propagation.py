import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *
from factor_graph import *
from belief_propagation import *

mrf = string2factor_graph('f1(a,b)f2(b,c,d)f3(c)')
f1 = factor(['a', 'b'],      np.array([[2,3],[6,4]]))
f2 = factor(['b', 'd', 'c'], np.array([[[7,2,3],[1,5,2]],[[8,3,9],[6,4,2]]]))
f3 = factor(['c'],           np.array([5, 1, 9]))
mrf.change_factor_distribution('f1', f1)
mrf.change_factor_distribution('f2', f2)
mrf.change_factor_distribution('f3', f3)

bp = belief_propagation(mrf)
print(bp.belief('b').get_distribution())