import asyncio
import enum
import pygame# initilize the pygame module
from pygame.locals import *
import draw
import time
from util import box_states
from com import Com

game_duration = 10 * 60 * 1000 # 30 minutes
start_time = (time.time() * 1000) + game_duration

game_state = [box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED, box_states.UNSOLVED]

class Game(object):
    def __init__(self):
        self.execute_time = 0
        self.running = True

        pygame.init()# Setting your screen size with a tuple of the screen width and screen height
        pygame.display.set_caption("Safer Escape Room")# Update your screen when required

        self.surface = pygame.display.set_mode((1920,1080), HWSURFACE|DOUBLEBUF|RESIZABLE)# Setting a random caption title for your pygame graphical window.
        self.work_surface = self.surface.copy()

    def state_translate(self, node_state):

        if node_state[0] == 1: # GS_A
            game_state[0] = box_states.IN_PROGRESS
            game_state[1] = box_states.UNSOLVED
            game_state[2] = box_states.UNSOLVED
            game_state[3] = box_states.UNSOLVED
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 2: # GS_B
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.IN_PROGRESS
            game_state[2] = box_states.UNSOLVED
            game_state[3] = box_states.UNSOLVED
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 3: # GS_B_TIMEOUT
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.TIMEOUT
            game_state[2] = box_states.UNSOLVED
            game_state[3] = box_states.UNSOLVED
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 4: # GS_C
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.IN_PROGRESS
            game_state[3] = box_states.UNSOLVED
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 5 or node_state[0] == 6: # GS_D
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.SOLVED
            game_state[3] = box_states.IN_PROGRESS
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 7: # GS_D_TIMEOUT
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.SOLVED
            game_state[3] = box_states.TIMEOUT
            game_state[4] = box_states.UNSOLVED
        elif node_state[0] == 8 or node_state[0] == 9: # GS_E
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.SOLVED
            game_state[3] = box_states.SOLVED
            game_state[4] = box_states.IN_PROGRESS
        elif node_state[0] == 10: # GS_E_TIMEOUT
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.SOLVED
            game_state[3] = box_states.SOLVED
            game_state[4] = box_states.TIMEOUT
        elif node_state[0] == 11: # GS_E_TIMEOUT
            game_state[0] = box_states.SOLVED
            game_state[1] = box_states.SOLVED
            game_state[2] = box_states.SOLVED
            game_state[3] = box_states.SOLVED
            game_state[4] = box_states.SOLVED
        else:
            game_state[0] = box_states.UNSOLVED
            game_state[1] = box_states.UNSOLVED
            game_state[2] = box_states.UNSOLVED
            game_state[3] = box_states.UNSOLVED
            game_state[4] = box_states.UNSOLVED

    async def tick(self, node_state):
        self.state_translate(node_state)
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                surface = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)

        self.execute_time = (time.time() * 1000)
        self.delta_time = start_time - self.execute_time

        draw.timer_text(pygame, self.work_surface, self.delta_time, warning_minute=5)
        draw.timer_decals(pygame, self.work_surface, self.delta_time, warning_minute=5)
        draw.timer_line(pygame, self.work_surface, self.delta_time, game_duration)
        draw.stage_boxes(pygame, self.work_surface, game_state)
        self.surface.blit(pygame.transform.scale(self.work_surface, self.surface.get_rect().size), (0, 0))
        pygame.display.update() # quit the pygame initialization and module
        if(self.running == False):
            pygame.quit() # End the program
            quit()