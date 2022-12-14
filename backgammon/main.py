# main.py
# Run file to start game

from threading import Thread

import pygame

from bot import Bot
from field import Field
from player import Player

SIZE = (1000, 935)  # size of screen
FPS = 30  # max fps

clock = pygame.time.Clock()  # clock

screen = pygame.display.set_mode(SIZE)  # screen

f = Field(screen, SIZE, None)  # field

player1 = Player(f)  # player
player2 = Bot(f)  # bot

f._players = (player1, player2)  # set players

Thread(target=f.start, args=(), daemon=True).start()  # start game

is_running = True  # is running flag

while is_running:
    f.print()  # print all
    pygame.display.update()  # update display
    clock.tick(FPS)  # wait
    
    for event in pygame.event.get():  # handle events
        match event.type:  # match event type
            case pygame.QUIT:  # quit event
                is_running = False
                break
            
            case pygame.MOUSEMOTION:  # mousemotion event
                player1.move_mouse(event.pos)  # move mouse
                player1.mousemotion_event_handler(event.pos)  # handle event
            
            case pygame.MOUSEBUTTONDOWN:  # mousebuttondown event
                player1.mousebuttondown_event_handler(event.pos)  # handle event
