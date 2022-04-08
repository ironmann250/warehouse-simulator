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
        self.running=True
        self.instruction_counter=0
        self.clock=pygame.time.Clock()
        self.grid_size=[0,0] #x,y number of cells in grid
        self.inputs=[]
        self.outputs=[]
        self.crates=[]
        self.grid=[]
        self.crane=[0,0]
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
        self.grid[self.crane[0]][self.crane[1]]=[4,Container((config.CRANE_COLOR),self.get_cell_coordinate(self.crane[0],self.crane[1]))]

        # init inputs
        gridy=1
        gridx=input_start_at
        
        for i in range(config.INPUT):
            for j in range (config.INPUT_CONTAINERS):

                self.inputs.append(Container(config.INPUTS_COLOR,
                self.get_cell_coordinate(gridx,gridy)))

                self.grid[gridx][gridy]=[2,Container(config.INPUTS_COLOR,
                self.get_cell_coordinate(gridx,gridy))] #put type and list location

                gridx+=1
            gridx+=1 # skip a cell

        # init inputs
        gridy=rows-1
        gridx=output_start_at

        for i in range(config.OUTPUTS):
            for j in range (config.OUTPUT_CONTAINERS):

                self.outputs.append(Container(config.OUTPUTS_COLOR,
                self.get_cell_coordinate(gridx,gridy)))

                self.grid[gridx][gridy]=[3,Container(config.OUTPUTS_COLOR,
                self.get_cell_coordinate(gridx,gridy))] #put type and list location
                gridx+=1
            gridx+=1 # skip a cell
        
        #init crates 
        gridy=crates_y_start_at
        gridx=crates_x_start_at

        for group in range(config.CRATES_GROUPS):
            for length in range(config.CRATES_LENGTH):
                for width in range(config.CRATES_WIDTH):
                    if config.CRATES[group][length][width] == 1:
                        
                        self.crates.append(Container(config.CRATES_COLOR,
                        self.get_cell_coordinate(gridx,gridy)))

                        self.grid[gridx][gridy]=[1,Container(config.CRATES_COLOR,
                        self.get_cell_coordinate(gridx,gridy))]
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
        for rows in self.grid:
            for col in rows:
                if col[0]!=0:
                    self.screen.blit(col[1].surf,col[1].rect)
    
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
        #move and destroy last one
        self.grid[curr_location[0]][curr_location[1]]=[0,0]
        self.grid[self.crane[0]][self.crane[1]]=[4,Container((config.CRANE_COLOR),
        self.get_cell_coordinate(self.crane[0],self.crane[1]))]
        


                

                

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
    pygame.display.set_caption("warehouse simulator")
    sim=Screen()
    
    sim.run()