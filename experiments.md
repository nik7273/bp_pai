Experiments for Kitchen for Progress 2D
============
## Metrics
- efficiency (time spent planning, number of moves taken to complete a goal)
- success (number of successful planning trials (did it find the solution?))
- generality (what types of problems can the planner solve and what can't it solve?)
- how confident is it when it solves the problem?

## Questions
- How detailed must these plan skeletons be? (ask about forward search)  
- 

## Box2D
Testing:
- increase the complexity of the problem
    - lower random probability of objects existing within drawers (how much uncertainty we start with)
        - maybe use cross entropy to systematically increase complexity?
    - increase the number of possible tasks (how many actions we have)
    - increase the number of objects (how many symbols we have)

## PyBullet
Differences between PyBullet and K2D:
- we're including motion planning


# Setup Designs
## 2D
Our default: (3 cups, faucet, 3 drawers)

3 concrete tasks:
- Pick correct cups from drawer and mix their liquids
- use one from Kitchen2D?
- uncertainty in sizes of cups
- give instructions: how much water, infer the optimal cup size to pick


- drawer task
    - cup -> which drawer it's located in
    - ex. pick the cup in the first drawer

- uncertainty in action success
    - ex. gripper can successfully grip the cup with some probability < 1

- uncertainty in amount of time spent under x faucet
    - liquid -> how much time to stay under its faucet
    - goal: mix appropriate amount of respective liquids (ex. 10mL sugar + 20 mL water)
    - example prior distribution:
    - sugar: 1: 10%, 2, 3
    - water: 1, 2, 3

- vary the priors
    - imagine the gripper is nearly certain about the wrong answer
    - probably do this for every run of a given experiment, since using the same prior everytime will likely give a deterministic result

- algorithm stability: keep 2 identical cups in the drawers and see what happens to the algorithm

Things to do:
- track the number of steps taken
- track the *mean* and *variance* of the number of steps taken
- track number of times task completes successfully
- possibly track time taken (seems dependent on hardware, so test on a standard setup)

- fix action == 'Fin' at end for failure case


## 3D


