from maze import Maze, MazeLocation, manhattan_distance
from generic_search import node_to_path, astar, Node
from typing import List,Callable, Optional
import time
from copy import deepcopy
#module to handle minimax simulation of the grid
#a more optimized implementation of grid action
#performed by the interface (screen) module
#also not using any pygame functions because
#they can't be pickled(deepcopy)
#also no loops if possible :)

class Grid():
    def __init__(self,grid=[[[]]],crane=[0,0,0],instructions=[]):
        self.grid=deepcopy(grid)
        self.crane=deepcopy(crane)
        self.grid_size=[len(grid),len(grid[0])]
        self.instructions=instructions
        self.instruction_counter=0
        #print (self.instructions)
        #print ("#########################")

    ### methods it should have ###
    #execute instructions
    #-> read instructions
    #-> plan path
    #-> path execution
    #-> move_crane
    #-> detect collision
    #-> perform crane action


    def collision_detected(self,next):
        next_cell=self.grid[next[0]][next[1]]
        if next_cell[0] in [1,2,3]:
            return True
        else:
            return False
    

    def auto_crane_action(self,next): 
        """
        if it's a crate and crane is empty add in crate in crane else do nothing
        if it's input and crane is empty and the input (empty ) crate else do nothing
        if it's output and it has a crate and crane is empty add it otherwise do nothing
        after adding things to the crane make input or output empty
        output will be emptied automatically following a time based event
        input will be replenished following a time based event as well
        """
        next_cell=self.grid[next[0]][next[1]]
        if self.crane[2]==0: #crane is empty
            if next_cell[0]==1 and next_cell[1]!=0: 
                #if it's a crate and not empty
                #add to crate and make holder empty
                self.crane[2]=1
                self.grid[next[0]][next[1]]=[1,0]
            if next_cell[0]==2 and next_cell[1]!=0:
                #if it's input and not empty
                #add to crane and make input empty
                self.crane[2]=1
                self.grid[next[0]][next[1]]=[2,0]
        else:
            if next_cell[0]==1 and next_cell[1]==0: 
                #if it's a crate and empty
                #remove from crane and make crate full
                self.crane[2]=0
                self.grid[next[0]][next[1]]=[1,1]
            if next_cell[0]==3 and next_cell[1]==0:
                #if it's output empty
                self.crane[2]=0
                self.grid[next[0]][next[1]]=[3,1]

    def move_crane(self, direction):
        curr_location=self.crane.copy()
        #do move
        if direction=='up':
            self.crane[1]-=1
        elif direction=='down':
            self.crane[1]+=1
        elif direction=='left':
            self.crane[0]-=1
        elif direction=='right':
            self.crane[0]+=1

        #check signs and border
        if self.crane[0]<0:
            self.crane[0]=0
        elif self.crane[0]>self.grid_size[0]:
            self.crane[0]=self.grid_size[0]
        if self.crane[1]<0:
            self.crane[1]=0
        elif self.crane[1]>self.grid_size[1]:
            self.crane[1]=self.grid_size[1]
        #check move validity and function
        if not self.collision_detected(self.crane):
            #move and destroy last one
            self.grid[curr_location[0]][curr_location[1]][1]=0
            #self.grid[self.crane[0]][self.crane[1]]=[4,1]
            #self.crane[2]=1
        else:
            self.auto_crane_action(self.crane)
            #move it back but keep empty state [2]
            self.crane[0]=curr_location[0]
            self.crane[1]=curr_location[1]

    def plan_path(self,start,end):
        #print ("calculation path from ",start,"to",end,"...")
        c=time.time()
        start = MazeLocation(start[0],start[1])
        end = MazeLocation(end[0],end[1])

        mz=Maze(grid=self.grid,rows=len(self.grid),
        columns=len(self.grid[0]),start=start,goal=end)

        distance: Callable[[MazeLocation], float] = manhattan_distance(mz.goal)

        solution: Optional[Node[MazeLocation]] = astar(mz.start, 
        mz.goal_test, mz.successors,distance)

        if solution is None:
            print ("calculation invalid")
            return []
        else:
            path: List[MazeLocation] = node_to_path(solution)
            print ("calculation finished in: ",time.time()-c ,"seconds")
            return path

    def path_result(self,action,path):
        if path==[]:
            return self.grid
        last_cell=path[-1]
        self.crane[0]=last_cell.row
        self.crane[1]=last_cell.column
        self.move_crane(action)
        return deepcopy(self.grid)
        

    def execute_instruction(self,instruction):
        start,end,action=instruction
        if start==self.crane[:2]:
            return self.path_result(action, self.plan_path(start, end)) #a grid
            

    def run(self):
        grids=[]
        #loop is ok cause it's small usually 2 loops
        for instruction in self.instructions:
            #print (instruction)
            grids.append(self.execute_instruction(instruction))
        return grids



