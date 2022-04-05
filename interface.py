import pygame,config,random

from pygame.locals import (

    K_LEFT,
    K_RIGHT,
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
class Crate(pygame.sprite.Sprite):
    """
    create crate object
    """
    def __init__(self,color):
        super(Crate,self).__init__()
        self.surf = pygame.Surface(config.BLOCK_SIZE)
        self.surf.fill(color)
        self.rect=self.surf.get_rect()

class Screen:
    def __init__(self):
        pygame.init()
        self.screen=pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        self.running=True
        self.instruction_counter=0
        self.clock=pygame.time.Clock()

    def draw_rect(self,color,x,y,width,height):
        pygame.draw.rect(self.screen,color,
                pygame.Rect(x, y,width,height))

    def draw_grid(self):
        """
        create background grid
        """
        width_left=0
        line_length=config.SCREEN_HEIGHT
        height_left=0
        while ((height_left + width_left) < (config.SCREEN_HEIGHT+config.SCREEN_WIDTH)):

            if width_left<config.SCREEN_WIDTH:

                self.draw_rect((0,0,0),
                width_left,height_left,
                config.TABLE_LINE,config.SCREEN_HEIGHT)

                width_left+=(config.BLOCK_SIZE[0]+config.TABLE_LINE)
            else:
                width_left=config.SCREEN_WIDTH

                self.draw_rect((0,0,0),
                0,height_left,
                config.SCREEN_WIDTH,config.TABLE_LINE)

                height_left+=(config.BLOCK_SIZE[1]+config.TABLE_LINE)


        print (width_left,height_left)
    
    def draw_frame(self):
        self.screen.fill((255,255,255))
        self.draw_grid()
       
        pygame.display.update()
    
    def run(self):
        while self.running:
            
            self.draw_frame()
            #self.clock.tick(120)

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
        pygame.quit()


if __name__ == "__main__":
    pygame.display.set_caption("warehouse simulator")
    sim=Screen()
    sim.run()