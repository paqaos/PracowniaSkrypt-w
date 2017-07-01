#!/usr/bin/python

import pygame
from pygame.locals import *
import Tower
import Game

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((768, 640))
    pygame.display.set_caption('Basic Pygame program')

    # Fill background
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((126, 51, 0))

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("Hello There", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    ## background.blit(text, textpos)

    # Blit everything to the screen
    screen.blit(background, (0, 0))

    pygame.display.flip()

    game = Game.GameManager()
    game.setFont(font)
    game.setGuiSurface(background)

    clock = pygame.time.Clock()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return
            if event.type == KEYDOWN and game.process_input(event) == False:
                return

        game.update()

        screen.blit(background, (0, 0))

        game.render(screen)

        pygame.display.flip()
        clock.tick(45)


if __name__ == '__main__': main()