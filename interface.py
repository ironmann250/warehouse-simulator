from tkinter import TRUE
import pygame,config,time

from pygame.locals import (

    K_LEFT,
    K_RIGHT,
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)



#make crates
#make output crates
#make input crates
#make crane (crane make line to move on)
#make all group
#make crates group
#make input group
#make output group
#make collission 
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
        pygame.init()
        self.screen=pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        pygame.display.set_caption("warehouse simulator")
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

                self.grid[gridx][gridy]=[2,1] #put type and list location
                gridx+=1
            gridx+=1 # skip a cell

        # init inputs
        gridy=rows-1
        gridx=output_start_at

        for i in range(config.OUTPUTS):
            for j in range (config.OUTPUT_CONTAINERS):

                self.grid[gridx][gridy]=[3,1] #put type and list location
                gridx+=1
            gridx+=1 # skip a cell
        
        #init crates 
        gridy=crates_y_start_at
        gridx=crates_x_start_at

        for group in range(config.CRATES_GROUPS):
            for length in range(config.CRATES_LENGTH):
                for width in range(config.CRATES_WIDTH):
                    if config.CRATES[group][length][width] == 1:
                        
                        self.grid[gridx][gridy]=[1,1]
                    else:
                        self.grid[gridx][gridy]=[1,0]
                    #print(config.CRATES[group][length][width] )
                    gridx+=1
                gridx=crates_x_start_at
                gridy+=1
            crates_x_start_at+=(config.CRATES_WIDTH+1)
            gridx=crates_x_start_at
            gridy=crates_y_start_at
        print(len(self.grid),len(self.grid[0]))
        self.init=False #stop init (only run at startup)

    def draw_components(self):
        r=0
        for rows in self.grid:
            c=0
            for col in rows:
                if col[0]!=0:
                    if col[1]!=0: #col[1] is NOT empty in case of empty crates,inputs and outputs
                        obj=None
                        if col[0]==1:
                            obj=Container(config.CRATES_COLOR,self.get_cell_coordinate(r,c))
                        elif col[0]==2:
                            obj=Container(config.INPUTS_COLOR,self.get_cell_coordinate(r,c))
                        elif col[0]==3:
                            obj=Container(config.OUTPUTS_COLOR,self.get_cell_coordinate(r,c))
                        elif col[0]==4:
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

    def auto_crane_action(self,current,next): 
        """
        if it's a crate and crane is empty add in crate in crane else do nothing
        if it's input and crane is empty and the input (empty ) crate else do nothing
        if it's output and it has a crate and crane is empty add it otherwise do nothing
        after adding things to the crane make input or output empty
        output will be emptied automatically following a time based event
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
            self.grid[curr_location[0]][curr_location[1]]=[0,0]
            self.grid[self.crane[0]][self.crane[1]]=[4,1]
        else:
            self.auto_crane_action(curr_location,self.crane)
            #move it back but keep empty state [2]
            self.crane[0]=curr_location[0]
            self.crane[1]=curr_location[1]
            return
             
    def draw_frame(self):
        self.screen.fill((255,255,255))
        self.draw_grid()
        self.init_components()
        self.draw_components()
        pygame.display.update()
    
    def run(self):
        while self.running:
            
            self.draw_frame()
            self.clock.tick(120)

            #get left to rewind
            #get right to advance

            #create grid

            #render all entities

            #read and exec instruction
            #check collission
            #update robot
            #update crates
            #update inputs
            #update outputs

            #update instruction counter

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()


if __name__ == "__main__":
    
    sim=Screen()
    
    sim.run()