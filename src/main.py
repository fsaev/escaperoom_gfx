import asyncio
import enum
import pygame# initilize the pygame module
from pygame.locals import *
import draw
import time
from util import box_states
from com import Com

class commands(enum.IntEnum):
    CMD_SYNC = 0,
    CMD_START = 1,
    CMD_OVERRIDE = 2,
    CMD_STOP = 3

#com = Com("COM17")

game_duration = 5.2 * 60 * 1000 # 30 minutes
start_time = (time.time() * 1000) + game_duration

game_state = [box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED]

async def gfx_worker():
    execute_time = 0
    running = True

    pygame.init()# Setting your screen size with a tuple of the screen width and screen height
    surface = pygame.display.set_mode((1920,1080), HWSURFACE|DOUBLEBUF|RESIZABLE)# Setting a random caption title for your pygame graphical window.
    work_surface = surface.copy()
    pygame.display.set_caption("Safer Escape Room")# Update your screen when required

    while(running):
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                surface = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

        if((time.time() * 1000) - execute_time > 30): # frame limiter
            #pack = com.get_package()
            # if(pack):
            #     if(pack[0] == commands.CMD_SYNC):
            #         for i in range(0, len(pack[1])):
            #             game_state[i] = pack[1][i]

            execute_time = (time.time() * 1000)
            delta_time = start_time - execute_time

            draw.timer_text(pygame, work_surface, delta_time, warning_minute=5)
            draw.timer_decals(pygame, work_surface, delta_time, warning_minute=5)
            draw.timer_line(pygame, work_surface, delta_time, game_duration)
            draw.stage_boxes(pygame, work_surface, game_state)
            surface.blit(pygame.transform.scale(work_surface, surface.get_rect().size), (0, 0))
            pygame.display.update() # quit the pygame initialization and module
        if(running == False):
            pygame.quit() # End the program
            quit()

if __name__ == "__main__":
    asyncio.run(gfx_worker())
