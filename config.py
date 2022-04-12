import random,pprint

SCREEN_WIDTH=860
SCREEN_HEIGHT=650
TABLE_LINE=1
BLOCK_SIZE=[20,20]
#gives us grid size of 40 by 30 (x by y blocks)

#colors for blocks mean black/white is empty others mean full
CRANE_REACH=3
CRANE_SPEED=5
CRANE_COLOR=(255,116,64) ##ff7440, redorange

INPUT=2
INPUT_CONTAINERS=8
INPUT_SPEED=15000 #milliseconds
INPUTS_COLOR=(0,255,0)


OUTPUTS=2
OUTPUT_CONTAINERS=8
OUTPUT_SPEED=20000 #milliseconds
OUTPUTS_COLOR=(255,0,0)

CRATES_WIDTH=2
CRATES_LENGTH=20
CRATES_GROUPS=5
CRATES=[[[0]*CRATES_WIDTH]*CRATES_LENGTH
 for i in range(CRATES_GROUPS)] #init crates GROUP[LENGTH[WIDTH]]
CRATES_COLOR=(0,0,255)

EMPTY_COLOR=(211,211,211)

TYPES=[0,1,2,3] #0 nothing, 1 crate, 2 input, 3 output, 4 is robot
INSTRUCTIONS=[]
'''[[[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up'],
             [[0,0],[17,25],'up'],  #[[FROM], [TO]] ID is what grid to what grid
             [[17,25],[16,25],'up'],
             [[16,25],[0,0],'up']
             ]'''

MIN_MAX_ORDERS=[1,5]

def randomly_populate_crates():
    for group in range(CRATES_GROUPS):
        for length in range(CRATES_LENGTH):
            for width in range(CRATES_WIDTH):
                #choose randomly with bias of n% for a crate to not be empty
                CRATES[group][length][width]=random.choices([1,0], weights=(100,0),k=1)[0] 


randomly_populate_crates()

#pprint.pprint(CRATES)



