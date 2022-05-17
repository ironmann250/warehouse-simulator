# given a grid, crane starting position, inputs, outputs and crates
# make instructions for the crane to get inputs to crates, 
# crates to outputs and handle orders
# orders are users submitting orders of particular number of crates
# the crane executess each order one by one
# the crane will pause if outputs are full then continue after

import config,random,pprint
from copy import copy as deepcopy
from grid_container import Grid
order_count=0

class Grid_stats():
    def __init__(self,grid=[[[]]],instructions=[]):
        self.full_inputs=0
        self.total_inputs=0
        self.empty_inputs=0
        self.full_outputs=0
        self.total_outputs=0
        self.empty_outputs=0
        self.full_crates=0
        self.total_crates=0
        self.empty_crates=0
        self.instructions=instructions
        grid=deepcopy(grid)
        for r,rows in enumerate(grid):
            for c,col in enumerate(rows):
                if col[0]==2:
                    self.total_inputs+=1
                    if col[1]==1:
                        self.full_inputs+=1
                    else:
                        self.empty_inputs+=1
                if col[0]==1:
                    self.total_crates+=1
                    if col[1]==1:
                        self.full_crates+=1
                    else:
                        self.empty_crates+=1

                if col[0]==3:
                    self.total_outputs+=1
                    if col[1]==1:
                        self.full_outputs+=1
                    else:
                        self.empty_outputs+=1

    def calculate_score(self,scoring_technique=1):
        """
        we evaluate the score based on the score equations
        output score = (total output - empty outputs) / total output
        input score = (total input - full inputs) / total input
        crates score is more trickier cause we want the score to be
        almost always high and drop very fast when it's gonna be full
        or we want it high only when the crates are balanced
        so we get the 0 - 1 ratio as we did for the rest but add equations
        that make it fit either of those 2 cases

        crate score equation 1 = 0.0476 + crates_ratio / (crates_ratio + 5)
        crate score equation 2 = 1 - crates_ratio^2

        and we can have 2 resultant scores:
        score 1 = total_outputs + (crate score 1 * input score)
        this makes sure input is high until crates are almost full
        it will be between 0 and 2

        score 2 = total_outputs + crate score 2 + input score
        this balances the crates it is between 0 to 3

        score 3 = total_outputs + crate ratio + input score
        this balances the crates it is between 0 to 3
        """
        input_score = (self.total_inputs - self.empty_inputs)/self.total_inputs
        output_score = (self.total_outputs - self.full_outputs)/self.total_outputs
        crate_ratio = (self.total_crates - self.full_crates)/self.total_crates #0 if full 1 if empty
        score=0
        if scoring_technique == 1:
            crate_score=0.0476 + (crate_ratio*100) / ((crate_ratio*100) + 5)
            score = output_score + (crate_score * input_score)
        elif scoring_technique == 2:
            crate_ratio = (self.total_crates - self.full_crates)/self.total_crates
            mapped_crate_ratio=(crate_ratio*2)-1 #map it between -1 and 1
            crate_score=1-(mapped_crate_ratio**2)
            score = output_score + crate_score + input_score
        elif scoring_technique == 3:
            if output_score>0.5:
                output_score=0
            score = output_score + crate_ratio  +  (self.full_inputs*input_score)
            #print(score)
        else:
            score=0
            if self.total_outputs-self.empty_outputs>=4:
                score-=1
            else:
                score+=1
            if self.full_inputs !=0:
                if self.full_inputs in list(range(0,self.total_inputs+1)):
                    score+=1
        return score
    
    def stop_condition(self):
        if self.empty_inputs+self.empty_outputs+self.empty_crates==0:
            return True
        else:
            False

def make_crates_instruction(grid,start):
    #get full crates 
    crate=None
    #get output
    output=[]
    instructions=[]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==1 and col[1]==1 and not crate:
                crate=[r,c]
            elif col[0]==3:
                output.append([r,c])
            else:
                continue

    output=output[0]
    #make instruction
    if not crate or not output:
        return []
    #from start to crate
    end1=[crate[0]-1,crate[1]]
    action1='right'
    if grid[end1[0]][end1[1]][0]==1:
        end1=[crate[0]+1,crate[1]]
        action1='left'
    instructions.append([start,end1,action1])
    #from crate to output
    end2=[output[0],output[1]-1]
    action2='down'
    instructions.append([end1,end2,action2])

    return instructions

def make_input_instruction(grid,start):
    #get full crates 
    crate=None
    #get output
    input=None
    instructions=[]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==1 and col[1]==0 and not crate:
                crate=[r,c]
            elif col[0]==2 and col[1]==1 and not input:
                input=[r,c]
            else:
                continue
    #make instruction
    #get crate from input 
    if not crate or not input:
        return []
    end1=[input[0],input[1]+1]
    action1='up'
    instructions.append([start,end1,action1])
    #put crate in empty crate
    end2=[crate[0]-1,crate[1]]
    action2='right'
    if grid[end2[0]][end2[1]][0]==1:
        end2=[crate[0]+1,crate[1]]
        action2='left'
    instructions.append([end1,end2,action2])
    return instructions

def get_possible_moves(grid,crane):
    """
    moves => make_input_instruction(add to crates) 
    or make_crates_instruction(remove from crates)
    """
    grid1=deepcopy(grid)
    grid2=deepcopy(grid)
    crane1=deepcopy(crane)
    crane2=deepcopy(crane)

    store_instruction= make_input_instruction(grid1,crane1[:2])
    retrieve_instruction = make_crates_instruction(grid2,crane2[:2])
    
    
    store_sim_result=simulate_warehouse(grid1,crane1,store_instruction)
    retrieve_sim_result=simulate_warehouse(grid2,crane2,retrieve_instruction)


    store_result_stats=Grid_stats(store_sim_result[0],store_sim_result[1])
    print ("store score:",store_result_stats.calculate_score())
    retrieve_result_stats=Grid_stats(retrieve_sim_result[0],retrieve_sim_result[1])
    print ("retrieve score:",retrieve_result_stats.calculate_score())
    return [store_result_stats,retrieve_result_stats]



def simulate_warehouse(grid,crane,instructions):
    """
    move crane according to instructions and get new grid and crane
    """
    #using the optimized grid for minimax
    newGrid=Grid(grid,crane,instructions)
    if instructions:
        return [newGrid.run()[-1],instructions]
    else:
        return [grid,instructions]
    config.INSTRUCTIONS=instructions
    action=screen.execute_instruction()
    while action:
        screen.path_exec(action,0)
        action=screen.execute_instruction()
    screen.instruction_counter=0
    #config.INSTRUCTIONS=[]
    return [screen.grid,instructions]
    
toggle=0
def dumbminimax(move,depth,max_player,grid,crane):
    global toggle
    move=get_possible_moves(grid,crane)[1]
    # if toggle==0:
    #     toggle=1
    # else:
    #     toggle=0
    # print(toggle)
    return [],move

def make_decision(grid,crane):
    grid=deepcopy(grid)
    crane=deepcopy(crane)
    moves = get_possible_moves(grid,crane)
    if moves[0].calculate_score()>moves[1].calculate_score():
        return moves[0]
    else:
        return moves[1]

def decision_loop(grid,crane,depth):
    grid=deepcopy(grid)
    crane=deepcopy(crane)
    highest_score=float("-inf")
    best_move=Grid_stats(grid)
    for i in range(depth):
        for move in get_possible_moves(grid,crane):
            if move.calculate_score()>highest_score:
                best_move=move
                highest_score=best_move.calculate_score()
                #print(best_move.calculate_score())
    print("#######")
    print(best_move.calculate_score())
    return best_move


def minimax(move,depth,max_player,grid,crane):
    grid=deepcopy(grid)
    crane=deepcopy(crane)
    if depth <= 0 or move.stop_condition():
        #print (depth)
        return move.calculate_score(),move
    
    if max_player:
        maxEval = float("-inf") #maybe 0
        best_move=None
        for move in get_possible_moves(grid,crane):
            evaluation=minimax(move,depth-1,False,grid,crane)[0]
            maxEval = max(maxEval,evaluation)
            if maxEval == evaluation:
                best_move=move
            print (move.calculate_score())
        return maxEval,best_move
    else:
        minEval = float("inf") #maybe 3
        best_move=None
        for move in get_possible_moves(grid,crane):
            evaluation=minimax(move,depth-1,True,grid,crane)[0]
            minEval = min(minEval,evaluation)
            if minEval == evaluation:
                best_move=move
        #print (depth)
        return minEval,best_move

def randomized_time_dependent_action(grid,crane):
    grid=deepcopy(grid)
    crane=deepcopy(crane)
    grid_param=Grid_stats(grid)
    if grid_param.full_inputs == 0 and grid_param.full_outputs == 0:
        output_ratio=0
        input_ratio=1
    elif grid_param.full_inputs == 0 and grid_param.full_outputs != 0:
        output_ratio=0
        input_ratio=1
    elif (grid_param.full_crates/grid_param.total_crates>=random.uniform(0.9, 1)):
        output_ratio=0
        input_ratio=1
    elif (grid_param.empty_inputs/grid_param.total_inputs<=random.uniform(0, 0.2))or(grid_param.full_outputs/grid_param.total_outputs>=random.uniform(0.9, 1)):
        output_ratio=1
        input_ratio=0
    
    else :#grid_param.full_inputs != 0 and grid_param.full_outputs == 0:
        try:
            output_ratio=grid_param.full_outputs/grid_param.full_inputs#config.INPUT_SPEED/config.OUTPUT_SPEED
            input_ratio=grid_param.full_inputs/grid_param.full_outputs#config.OUTPUT_SPEED/config.INPUT_SPEED
        except:
            output_ratio=0.5
            input_ratio=0.5
    

    total=output_ratio+input_ratio
    
    if total!=0:
        output_perc=(output_ratio/total)*100
        input_perc=(input_ratio/total)*100
    else:
        input_perc=100
        output_perc=0
    choice=random.choices([1,0], weights=(input_perc,output_perc),k=1)[0] 
    #print (choice)
    return get_possible_moves(grid,crane)[choice]


def get_orders():
    min_,max_=config.MIN_MAX_ORDERS
    choices=list(range(min_,max_+1))
    return random.choice(choices)



def add_crate():
    #add crates, do it in interface
    #add crates from input on top of empty crates (first in last out)
    pass

#do order
#see if crates are empty and order_count>0 
#if empty add crates
#else
#take bottom crates and put in outputs
#wait or add inputs if outputs is full
#decrement order_count

def get_updated_crates(grid,crates):
    total_crates=0
    tot_grid=0
    tot_crate=0
    for g,group in enumerate(crates):
        for l,length in enumerate(group):
            for w,width in enumerate(length):
                row,column,status=crates[g][l][w]
                tot_crate+=status
                #print(crates[g][l][w], grid[row][column])
                crates[g][l][w][2]=grid[row][column][1]
                if grid[row][column][1] == 1:
                    total_crates+=1
                    tot_grid+=1
    print (tot_grid,tot_crate)
    #return total_crates,crates

def update_grid(grid,crates):
    for g,group in enumerate(crates):
        for l,length in enumerate(group):
            for w,width in enumerate(length):
                row,column,status=crates[g][l][w]
                grid[row][column][1]=status
                #print (status)
                #print(grid[row][column],crates[g][l][w])
    return grid #is it needed since we will work on self.grid?

def make_all_crates_empty(crates):
    for g,group in enumerate(crates):
        for l,length in enumerate(group):
            for w,width in enumerate(length):
                #crates[g][l][w][2]=0
                width[2]=0
                #print (width)
    return crates
            


def organize_crates(grid,crates):
    #reoraganize crates
    #put all crates near outputs
    #crates are given through the updated crates
    #total_crates,crates=get_updated_crates(grid.copy(),crates.copy())
    empty_crates=make_all_crates_empty(crates.copy())
    groups=config.CRATES_GROUPS
    tot_length=config.CRATES_LENGTH
    tot_width=config.CRATES_WIDTH
    #print("###########################################")
    #print (update_grid(grid.copy(),empty_crates.copy()))
    return update_grid(grid.copy(),empty_crates.copy()).copy()
    #populate low first
    #meaning loop is Length, width then Group, length=length-1
    for length in range(tot_length-1,-1,-1):
        for group in range(groups):
            for width in range(tot_width):
                if True:#total_crates>0:
                    empty_crates[group][length][width][2]=0
                    total_crates-=1

    

def get_inputs(grid,reverse=True):
    #get inputs location
    #loop and get location of crates and status
    empty_crates,full_crates=[[],[]]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==2:
                if col[1]!=0:
                    full_crates.append([r,c])
                else:
                    empty_crates.append([r,c])
    if reverse:
        full_crates.reverse()
        empty_crates.reverse()
    return full_crates,empty_crates


def get_outputs(grid,reverse=True):
    #get outputs location
    #loop and get location of crates and status
    empty_crates,full_crates=[[],[]]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==3:
                if col[1]!=0:
                    full_crates.append([r,c])
                else:
                    empty_crates.append([r,c])
    if reverse:
        full_crates.reverse()
        empty_crates.reverse()
    return full_crates,empty_crates




def get_grid_stats(grid):
    full_inputs,empty_inputs,total_inputs=[0,0,0]
    full_crates,empty_crates,total_crates=[0,0,0]
    full_outputs,empty_outputs,total_outputs=[0,0,0]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==2:
                total_inputs+=1
                if col[1]==1:
                    full_inputs+=1
                else:
                    empty_inputs+=1
            if col[0]==1:
                total_crates+=1
                if col[1]==1:
                    full_crates+=1
                else:
                    empty_crates+=1

            if col[0]==3:
                total_outputs+=1
                if col[1]==1:
                    full_outputs+=1
                else:
                    empty_outputs+=1

    grid_stats=Grid_stats()
    grid_stats.full_inputs=full_inputs
    grid_stats.total_inputs=total_inputs
    grid_stats.empty_inputs=empty_inputs
    grid_stats.full_outputs=full_outputs
    grid_stats.total_outputs=total_outputs
    grid_stats.empty_outputs=empty_outputs
    grid_stats.full_crates=full_crates
    grid_stats.total_crates=total_crates
    grid_stats.empty_crates=empty_crates
    return grid_stats


    

def simple_strategy(grid,start):
    #choose to store or retrieve if 
    # inputs reach or are under a ratio
    full_inputs,total_inputs=[0,0]
    full_crates,total_crates=[0,0]
    full_outputs,total_outputs=[0,0]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==2:
                total_inputs+=1
                if col[1]==1:
                    full_inputs+=1
            if col[0]==1:
                total_crates+=1
                if col[1]==1:
                    full_crates+=1

            if col[0]==3:
                total_outputs+=1
                if col[1]==1:
                    full_outputs+=1
    
    print ("inputs ratio  : ",full_inputs/total_inputs)
    print ("crates ratio  : ",full_crates/total_crates)
    print ("outputs ratio : ",full_outputs/total_outputs)
    input_ratio,crate_ratio,output_ratio=[0/16,
          4/10,
           2/10]
    #minimize input ratio, mazimize output_ratio,
    #check the rate of change of crate too or maybe all ratios
    if full_inputs/total_inputs>input_ratio:
        return make_input_instruction(grid,start)
    else:
        return make_crates_instruction(grid,start)
    
    
                    
        