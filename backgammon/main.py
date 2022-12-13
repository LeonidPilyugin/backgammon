# main.py
# Run file to start game

from threading import Thread

import pygame

from bot import Bot
from field import Field
from player import Player

# clock
clock = pygame.time.Clock()
# size of screen
SIZE = (1000, 935)
# max fps
FPS = 30
# screen
screen = pygame.display.set_mode(SIZE)
# field
f = Field(screen, SIZE, None)
# players
player1 = Player(f)
player2 = Bot(f)
# set players
f._players = (player1, player2)
# start game
Thread(target=f.start, args=(), daemon=True).start()

# main cycle
is_running = True
while is_running:
    # print field
    f.print()
    pygame.display.update()
    # wait
    clock.tick(FPS)
    # handle events
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                is_running = False
                break
            case pygame.MOUSEMOTION:
                player1.move_mouse(event.pos)
                player1.mousemotion_event_handler(event.pos)
                player2.mousemotion_event_handler(event)
            case pygame.MOUSEBUTTONDOWN:
                player1.mousebuttondown_event_handler(event.pos)
                player2.mousebuttondown_event_handler(event)
