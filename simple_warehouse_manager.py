# given a grid, crane starting position, inputs, outputs and crates
# make instructions for the crane to get inputs to crates, 
# crates to outputs and handle orders
# orders are users submitting orders of particular number of crates
# the crane executess each order one by one
# the crane will pause if outputs are full then continue after

import config,random

order_count=0

def get_orders():
    min_,max_=config.MIN_MAX_ORDERS
    choices=list(range(min_,max_+1))
    return random.choice(choices)

for i in range (50):
    print (get_orders(),end=",")