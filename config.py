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
INPUT_SPEED=3
INPUTS_COLOR=(0,255,0)


OUTPUTS=2
OUTPUT_CONTAINERS=8
OUTPUT_SPEED=7
OUTPUTS_COLOR=(255,0,0)

CRATES_WIDTH=2
CRATES_LENGTH=5
CRATES_GROUPS=4
CRATES=[[[0]*CRATES_WIDTH]*CRATES_LENGTH
 for i in range(CRATES_GROUPS)] #init crates GROUP[LENGTH[WIDTH]]
CRATES_COLOR=(0,0,255)

TYPES=[0,1,2,3] #0 nothing, 1 crate, 2 input, 3 output, 4 is robot
INSTRUCTIONS=[] #[FROM_TYPE,FROM_ID,TO_TYPE,TO_ID] ID is what grid to what grid

def randomly_populate_crates():
    for group in range(CRATES_GROUPS):
        for length in range(CRATES_LENGTH):
            for width in range(CRATES_WIDTH):
                #choose randomly with bias of n% for a crate to not be empty
                CRATES[group][length][width]=random.choices([1,0], weights=(70,30),k=1)[0] 


randomly_populate_crates()

#pprint.pprint(CRATES)

print(CRATES[0])
print(CRATES[1])
print(CRATES[2])
print(CRATES[3])


