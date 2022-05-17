# warehouse-simulator
an automated storage/retrieval warehouse simulator, that controls a crane, has multiple input and outputs and solves an optimal path for the crane (path planning uses A* by default and plan the path as if it's solving a maze).

the amount of inputs, outputs, crates can be change, as well as their arrangement, also the frequency of input and output, colors and various other parameters check config.py to customize it.

# controls
the control keys are:
- a: to enable the AI
- s: to automatically store once
- r: to automatically retrieve once
- space: to put it in manual mode
- up,down,left,right: to move the crane only when in manual mode

sometimes when in AI mode you might need to press the keys multiple times, since the AI runs faster than the simulator.

# install

```sh
pip install pygame
```

# run

```sh
python interface.py
```