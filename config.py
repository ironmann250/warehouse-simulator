import random,pprint

SCREEN_WIDTH=800
SCREEN_HEIGHT=600
TABLE_LINE=5
BLOCK_SIZE=[40,20]

#colors for blocks mean black/white is empty others mean full
CRANE_REACH=3
CRANE_SPEED=5
CRANE_COLOR=(255,116,64) ##ff7440, redorange

INPUT=4
INPUT_BUFFER=8
INPUT_SPEED=3
INPUT_COLOR=(0,255,0)


OUTPUTS=4
OUTPUT_BUFFER=8
OUTPUT_SPEED=7
OUTPUTS_COLOR=(255,0,0)

CRATES_WIDTH=2
CRATES_LENGTH=5
CRATES=[]
CRATES_COLOR=(0,0,255)

INSTRUCTIONS=[] #[FROM_TYPE,FROM_ID,TO_TYPE,TO_ID]

def populate_crates():
    global CRATES_LENGTH, CRATES_WIDTH, CRANE_REACH
    CRATES=[]
    for i in range(CRATES_LENGTH):
        tmp=[]
        for j in range(CRATES_WIDTH):
            for k in range(CRANE_REACH):
                tmp.append(random.choices([0,1])) #choices 0 always mean nothing others mean crate is full
        CRATES.append(tmp)
    return CRATES

#pprint.pprint(populate_crates())


