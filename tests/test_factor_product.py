import sys
import os
script_path = os.path.dirname(os.path.realpath(__file__))
os.sys.path.append(os.path.realpath(script_path + '/../src/'))
from factor import *

print('\n ***Test 1***')
phi_1 = factor(['a','b'], np.array([[0.5, 0.8], [0.1, 0.0], [0.3, 0.9]]))
phi_2 = factor(['b','c'], np.array([[0.5, 0.7], [0.1,0.2]]))

phi_3 = factor_product(phi_1, phi_2)

print(phi_3.get_variables())
print(phi_3.get_distribution())

print('\n ***Test 2***')
phi_4 = factor(['a', 'b'], np.array([[0.3, 0.8], [0.2, 0.1], [0.5, 0.1]]))
phi_5 = factor(['b'], np.array([0.3, 0.7]))

phi_6 = factor_product(phi_1, phi_2)
print(phi_6.get_variables())
print(phi_6.get_distribution())