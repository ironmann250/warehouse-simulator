from enum import auto
import pygame,config,time,asyncio,collections,pprint
from maze import Maze, MazeLocation, manhattan_distance,euclidean_distance
from generic_search import dfs, bfs, node_to_path, astar, Node
from typing import List, NamedTuple, Callable, Optional
from simpleWarehouseManager import organize_crates,get_updated_crates,update_grid,make_all_crates_empty,make_instruction
#global vars
from pygame.locals import (

    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.display.set_caption("warehouse simulator")
time.sleep(0.05)
ADDTOINPUT = pygame.USEREVENT + 1
pygame.time.set_timer(ADDTOINPUT,config.INPUT_SPEED)
time.sleep(0.05)
REMOVEFROMOUTPUT = pygame.USEREVENT + 2
pygame.time.set_timer(REMOVEFROMOUTPUT, config.OUTPUT_SPEED)


class Container(pygame.sprite.Sprite):
    """
    create crate object
    """
    def __init__(self,color,coords):
        super(Container,self).__init__()
        self.surf = pygame.Surface(config.BLOCK_SIZE)
        self.surf.fill(color)
        self.rect=self.surf.get_rect(center=coords)
        

class Screen:
    def __init__(self):
        #init pygame attributes
        self.screen=pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        #init screen class attributes
        self.running=True
        self.instruction_counter=0
        self.clock=pygame.time.Clock()
        self.grid_size=[0,0] #x,y number of cells in grid
        self.inputs=[]
        self.outputs=[]
        self.crates=[]
        self.grid=[]
        self.containers=[]
        self.crane=[0,0,0] #grid x,y and content 0 nothing, 1 something
        self.init=True
        self.testrun=True
        self.path=[]
        self.path_counter=0

    def draw_rect(self,color,x,y,width,height):
        pygame.draw.rect(self.screen,color,
                pygame.Rect(x, y,width,height))

    def draw_grid(self):
        """
        create background grid
        """
        width_left=-config.TABLE_LINE
        line_length=config.SCREEN_HEIGHT
        height_left=-config.TABLE_LINE
        x,y=[0,0]
        while ((height_left + width_left) < (config.SCREEN_HEIGHT+config.SCREEN_WIDTH)):

            if width_left<config.SCREEN_WIDTH:

                self.draw_rect((0,0,0),
                width_left,height_left,
                config.TABLE_LINE,config.SCREEN_HEIGHT)

                width_left+=(config.BLOCK_SIZE[0]+config.TABLE_LINE)
                x+=1
            else:
                width_left=config.SCREEN_WIDTH

                self.draw_rect((0,0,0),
                0,height_left,
                config.SCREEN_WIDTH,config.TABLE_LINE)

                height_left+=(config.BLOCK_SIZE[1]+config.TABLE_LINE)
                y+=1
        #depending on grid size value might be [x-1,y-2] or [x,y-1]
        #it can as well be calcualted form screen, block and line sizes
        self.grid_size=[x-1,y-1]
        #print (x-1,y-1)
    
    def get_cell_coordinate(self,col,row,centered=True):
        """
        calculate true pixel value of grid cells and send centers if required
        formula = col*blocksize+tableline, row*blocksize+tableline
        """
        x=col*(config.BLOCK_SIZE[0]+config.TABLE_LINE)
        y=row*(config.BLOCK_SIZE[1]+config.TABLE_LINE)
        if not centered:
            return [x,y]
        else:
            x=x+(config.BLOCK_SIZE[0]//2)
            y=y+(config.BLOCK_SIZE[1]//2)
            return [x,y]



    def init_components(self):
        if not self.init: #only run at init
            return
        cols,rows=self.grid_size
        self.grid=[[[0,0]]*(rows+1) for i in range(cols+1)] #init grid with 0s
        #assume all are on  on line - will later change lines to crates_width
        total_inputs=config.INPUT*config.INPUT_CONTAINERS #assume all inlines are inputs
        total_outputs=config.OUTPUTS*config.OUTPUT_CONTAINERS
        input_start_at=(cols-(total_inputs+(config.INPUT-1)))//2
        output_start_at=(cols-(total_outputs+(config.OUTPUTS-1)))//2
        gridx,gridy=[0,0]
        total_crates_length=(config.CRATES_GROUPS*config.CRATES_WIDTH)+(config.CRATES_GROUPS-1)
        crates_x_start_at=(cols-total_crates_length)//2
        crates_y_start_at=(rows-config.CRATES_LENGTH)//2
        
        #init crane
        self.grid[self.crane[0]][self.crane[1]]=[4,1]

        # init inputs
        gridy=1
        gridx=input_start_at
        
        for i in range(config.INPUT):
            for j in range (config.INPUT_CONTAINERS):

                self.grid[gridx][gridy]=[2,0] #put type and list location
                gridx+=1
            gridx+=1 # skip a cell

        # init outputs
        gridy=rows-1
        gridx=output_start_at

        for i in range(config.OUTPUTS):
            for j in range (config.OUTPUT_CONTAINERS):
                self.grid[gridx][gridy]=[3,0]
                gridx+=1
            gridx+=1 # skip a cell
        
        #init crates 
        gridy=crates_y_start_at
        gridx=crates_x_start_at
        self.crates=[[[0]*config.CRATES_WIDTH]*config.CRATES_LENGTH for i in range(config.CRATES_GROUPS)]
        for group in range(config.CRATES_GROUPS):
            for length in range(config.CRATES_LENGTH):
                for width in range(config.CRATES_WIDTH):
                    if config.CRATES[group][length][width] == 1:
                        
                        self.grid[gridx][gridy]=[1,1]
                        self.crates[group][length][width]=[gridx,gridy,1]
                    else:
                        self.grid[gridx][gridy]=[1,0]
                        self.crates[group][length][width]=[gridx,gridy,0]
                 
                    gridx+=1
                gridx=crates_x_start_at
                gridy+=1
            crates_x_start_at+=(config.CRATES_WIDTH+1)
            gridx=crates_x_start_at
            gridy=crates_y_start_at
        #print(self.grid)

        self.init=False #stop init (only run at startup)

    def draw_components(self): 
        r=0
        for rows in self.grid:
            c=0
            for col in rows:
                if col[0]==5:
                    obj=Container((254,216,177),self.get_cell_coordinate(r,c))
                    self.screen.blit(obj.surf,self.get_cell_coordinate(r,c,False))
                    
                elif col[0] in [1,2,3,4]:
                    if col[1]==1: #col[1] is NOT empty in case of empty crates,inputs and outputs
                        obj=None
                        if col[0]==1:
                            obj=Container(config.CRATES_COLOR,self.get_cell_coordinate(r,c))
                            #self.screen.blit(obj.surf,self.get_cell_coordinate(r,c,False))
                        elif col[0]==2:
                            obj=Container(config.INPUTS_COLOR,self.get_cell_coordinate(r,c))
                            #self.screen.blit(obj.surf,self.get_cell_coordinate(r,c,False))
                        elif col[0]==3:
                            obj=Container(config.OUTPUTS_COLOR,self.get_cell_coordinate(r,c))
                            #self.screen.blit(obj.surf,self.get_cell_coordinate(r,c,False))
                        elif col[0]==4 and col[1]!=0:
                            obj=Container(config.CRANE_COLOR,self.get_cell_coordinate(r,c))
                        
                        self.screen.blit(obj.surf,self.get_cell_coordinate(r,c,False))
                        

                    else: #the crate is empty
                        empty_crate=Container(config.EMPTY_COLOR,self.get_cell_coordinate(r,c))
                        self.screen.blit(empty_crate.surf,self.get_cell_coordinate(r,c,False))
                c+=1
            r+=1
                


    def collision_detected(self,next):
        next_cell=self.grid[next[0]][next[1]]
        if next_cell[0] in [1,2,3]:
            return True
        else:
            return False

    def asrs_crane_action(self,current,next,action): 
        #action from asrs algorithm #TODO
        pass

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
            self.grid[self.crane[0]][self.crane[1]]=[4,1]
        else:
            self.auto_crane_action(self.crane)
            #move it back but keep empty state [2]
            self.crane[0]=curr_location[0]
            self.crane[1]=curr_location[1]
            return
    
    def remove_from_output(self):
        #look for outputs on grid and empty the first full one
        outputs=[]
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                if col[0]==3:
                    outputs.append([r,c,col[1]])
                #and col[1]==1:
                #     col[1]=1
                #     break
                
        for i,crate in enumerate(outputs):
            if i==0:
                r1,c1,state1=crate
                self.grid[r1][c1][1]=0
                continue
            r1,c1,state1=crate
            r2,c2,state2=outputs[i-1]

            #self.grid[r1][c1][1]=state2
            self.grid[r1][c1][1]=state2
        
            

    
    def add_to_input(self):
        #look for inputs on grid and fill the first empty one
        for row in self.grid:
            for col in row:
                if col[0]==2 and col[1]==0:
                    col[1]=1
                    return
             
    
    def handle_events(self,event_list):
        for event in event_list:
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == REMOVEFROMOUTPUT:
                self.remove_from_output()
            if event.type == ADDTOINPUT:
                self.add_to_input()
    
    def plan_path(self,start,end):
        print ("calculation path from ",start,"to",end,"...")
        c=time.time()
        start = MazeLocation(start[0],start[1])
        end = MazeLocation(end[0],end[1])

        mz=Maze(grid=self.grid,rows=len(self.grid),
        columns=len(self.grid[0]),start=start,goal=end)

        distance: Callable[[MazeLocation], float] = euclidean_distance(mz.goal)

        solution: Optional[Node[MazeLocation]] = astar(mz.start, 
        mz.goal_test, mz.successors,distance)

        if solution is None:
            print ("calculation invalid")
            return []
        else:
            path: List[MazeLocation] = node_to_path(solution)
            print ("calculation finished in: ",time.time()-c ,"seconds")
            return path
    
    def path_exec(self,action,sleep_for=0.05):
        if self.path == []:
            return
        
        i=self.path_counter
        cell=self.path[i]
        if not i==0:
            self.grid[self.path[i-1].row][self.path[i-1].column]=[5,0]
        self.grid[cell.row][cell.column]=[4,1]
        time.sleep(sleep_for)
        if self.path_counter >= len(self.path)-1:
            self.crane[0]=cell.row
            self.crane[1]=cell.column
            self.move_crane(action)
            self.path=[]
            self.path_counter=0
            self.instruction_counter+=1
        else:
            self.path_counter+=1

    def location_near_crate(self,location):
        #check up, dow,left,right and diagonals
        xdirs=[-1,1,0]
        ydirs=[-1,1,0]
        for x in xdirs:
            for y in ydirs:
                if self.grid[location[0]+x][location[1]+y][0] in [1,2,3]:
                    return True
        return False
    
    def get_crane_location(self):
        for r,rows in enumerate(self.grid):
            for c,col in enumerate(rows):
                if col[0]==4:
                    return r,c

    def execute_instruction(self):
        if self.instruction_counter>=len(config.INSTRUCTIONS):
            config.INSTRUCTIONS=make_instruction(self.grid,self.get_crane_location())
            self.instruction_counter=0
            return None
        start,end,action=config.INSTRUCTIONS[self.instruction_counter]
        if len(self.path)>0: #let path finish
            return action
        #check if start has a crane
        #check if end is near a crate and calc action (up,down...)
        if self.grid[start[0]][start[1]][0]==4:
            if True:#self.location_near_crate(end):
                self.path=self.plan_path(start,end)
                return action

        return None


    
    def run_once(self):
        if not self.testrun:
            return
        self.testrun=False

    def draw_frame(self):
        self.screen.fill((255,255,255))
        self.draw_grid()
        self.init_components()
        self.draw_components()
        action=self.execute_instruction()
        if action:
            self.path_exec(action,0.001)
        pygame.display.update()
    
    def run(self):
        while self.running:

            event_list=pygame.event.get()
            
            self.draw_frame()
            #self.clock.tick()

            keys=pygame.key.get_pressed()

            if keys[K_UP]:
                self.move_crane('up')
                time.sleep(0.1)
            if keys[K_DOWN]:
                self.move_crane('down')
                time.sleep(0.1)
            if keys[K_LEFT]:
                self.move_crane('left')
                time.sleep(0.1)
            if keys[K_RIGHT]:
                self.move_crane('right')
                time.sleep(0.1)

            self.handle_events(event_list)

        pygame.quit()


if __name__ == "__main__":

    sim=Screen()
    sim.run()