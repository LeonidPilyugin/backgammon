# main.py
# Run file to start game

from threading import Thread
from tkinter import *
from tkinter import messagebox

import pygame

from bot import Bot
from field import Field
from player import Player

SIZE = (1000, 935)  # size of screen
FPS = 30  # max fps

pygame.display.set_icon(pygame.image.load("images/black.png"))  # set icon
pygame.display.set_caption("Backgammon")  # set title

clock = pygame.time.Clock()  # clock

screen = pygame.display.set_mode(SIZE)  # screen

field = Field(screen, SIZE, None)  # field

player = Player(field)  # player
bot = Bot(field)  # bot

field._players = (player, bot)  # set players

game = Thread(target=field.start, args=(), daemon=True)
game.start()  # start game

is_running = True  # is running flag

while is_running:
    field.print()  # print all
    pygame.display.update()  # update display
    clock.tick(FPS)  # wait
    
    for event in pygame.event.get():  # handle events
        match event.type:  # match event type
            case pygame.QUIT:  # quit event
                if messagebox.askyesno(message="Do you want to exit?"):
                    is_running = False
                break
            
            case pygame.MOUSEMOTION:  # mousemotion event
                player.move_mouse(event.pos)  # move mouse
                player.mousemotion_event_handler(event.pos)  # handle event
            
            case pygame.MOUSEBUTTONDOWN:  # mousebuttondown event
                player.mousebuttondown_event_handler(event.pos)  # handle event
                
    if not game.is_alive():  # if game ended
        if messagebox.askyesno(title="You won" if field.winner is player else "Game over",
                               message="Play again?"):  # if user wants to play again
            field = Field(screen, SIZE, None)
            player = Player(field)  # player
            bot = Bot(field)  # bot
            field._players = (player, bot)  # set players
            game = Thread(target=field.start, args=(), daemon=True)
            game.start()  # start game
        else:  # else finish
            is_running = False