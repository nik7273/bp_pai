# bp_pai
## Probabilistic Inference for Task Planning under uncertainty. 

### Pre-requisites
Run the following commands to install required graph representation and interactive graph visualization packages
1. `pip install python-igraph`
2. `pip install pyvis`

You would also need to install `pygame` for the kitchen simulation using this command
`pip install pygame==1.9.2`

The belief propagation implementation draws heavily from Aleksei Krasikov's Belief Propagation tutorial: https://krashkov.com/belief-propagation/

A demo of BP-PAI used to plan for a coffee-making task.
![](make_coffee.gif)

### Updated
A version based on Kitchen2D with smoother animations. 
```
python src/test_planning.py
```
