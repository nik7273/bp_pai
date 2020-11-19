import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *

phi_1 = factor(['a','b'], np.array([[0.5, 0.8], [0.1, 0.0], [0.3, 0.9]]))
phi_2 = factor(['b','c'], np.array([[0.5, 0.7], [0.1,0.2]]))

phi_3 = factor_product(phi_1, phi_2)

phi_4 = factor_marginalization(phi_3, ['b'])
print(phi_4.get_variables())