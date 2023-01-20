import pygame as pg
import os
from states.state import State


class Game_World(State):
    def __init__(self, game):
        super().__init__(game)

        self.gras_bg = self.game.generate_background(pg.image.load(os.path.join('res', 'gras.png')))
        self.wood_bg = self.game.generate_background(pg.image.load(os.path.join('res', 'plank.png')))

        self.bg = self.gras_bg

        self.reset_bg = False

    def update(self, actions):
        self.game.all_sprites.update()

        if self.game.current_location == [0, 0, 1]:
            self.bg = self.wood_bg
        if self.game.current_location == [0, -1, 1]:
            self.game.current_location = [0, 0]
            self.game.player_obj.rect.centerx = self.game.width / 2
            self.game.player_obj.rect.centery = self.game.height - 50
            self.reset_bg = True
        if self.game.current_location != [0, 0]:
            self.reset_bg = True
        elif self.reset_bg:
            self.bg = self.gras_bg
            self.reset_bg = False

    def render(self, win):
        win.blit(self.bg, (0, 0))

        self.game.drawn_sprites.draw(win)
