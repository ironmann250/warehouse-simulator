# given a grid, crane starting position, inputs, outputs and crates
# make instructions for the crane to get inputs to crates, 
# crates to outputs and handle orders
# orders are users submitting orders of particular number of crates
# the crane executess each order one by one
# the crane will pause if outputs are full then continue after

import config,random,pprint

order_count=0

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


def make_instruction(grid,start):
    #get full crates 
    crate=None
    #get output
    output=None
    instructions=[]
    for r,rows in enumerate(grid):
        for c,col in enumerate(rows):
            if col[0]==1 and col[1]==1 and not crate:
                crate=[r,c]
            elif col[0]==3 and col[1]==0 and not output:
                output=[r,c]
            else:
                continue
    #make instruction
    
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



        