import pygame

from config import FG_COLOUR


class Sprite(pygame.sprite.Sprite):

    def getSprite(self):
        pass

    def getPower(self):
        pass

    def getPosition(self):
        pass

    def getName(self):
        pass

    def debug(self):
        pass

    def set_text(self, string, coordx, coordy, fontSize):  # Function to set text
        font = pygame.font.Font('freesansbold.ttf', fontSize)
        text = font.render(string, True, FG_COLOUR)
        textRect = text.get_rect()
        textRect.center = (coordx, coordy)
        return (text, textRect)
