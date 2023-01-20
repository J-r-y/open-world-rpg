import pygame as pg
import os
from states.pause_menu import Pause_Menu
from states.state import State
from player import Player
from object import Obj
from YAwareGroup import YAwareGroup


class Game_World(State):
    def __init__(self, game):
        super().__init__(game)

        self.gras_bg = self.game.generate_background(pg.image.load(os.path.join('res', 'gras.png')))
        self.wood_bg = self.game.generate_background(pg.image.load(os.path.join('res', 'plank.png')))

        self.bg = self.gras_bg
        self.bg_blur = pg.Surface((self.game.width, self.game.height), pg.SRCALPHA)
        self.bg_blur.fill((0, 0, 0, 110))

        self.reset_bg = False

        self.player_obj = Player(self.game, 32, 32, os.path.join('res', 'dante.png'), self.game.width / 2,
                                 self.game.height - 50)
        self.house_obj = Obj(self.game, (216, 216), os.path.join('res', 'house.png'), 1.5, self.game.width / 2,
                             self.game.height / 2 - 50, [0, 0])
        self.house_open_obj = Obj(self.game, (216, 216), os.path.join('res', 'house_open.png'), 1.5, self.game.width / 2,
                                  self.game.height / 2 - 50, [0, 0])

        self.schrank_obj = Obj(self.game, (120, 128), os.path.join('res', 'schrank.png'), 1, 64, 66, [0, 0, 1])
        self.work_table_obj = Obj(self.game, (160, 120), os.path.join('res', 'work_table.png'), 0.875, 210, 60,
                                  [0, 0, 1])
        self.bed_obj = Obj(self.game, (75, 52), os.path.join('res', 'bed2.png'), 2, self.game.width - 80, 60,
                           [0, 0, 1])

        self.all_sprites = pg.sprite.Group(self.house_obj, self.schrank_obj, self.work_table_obj,
                                           self.bed_obj)
        self.furniture_sprites = pg.sprite.Group(self.schrank_obj, self.work_table_obj, self.bed_obj)
        self.drawn_sprites = YAwareGroup(self.player_obj, self.house_obj)

        self.game.actions["escape"] = False

    def update(self):
        self.player_obj.update(self.furniture_sprites)
        if self.player_obj.house_action == "open":
            self.load_sprite(self.house_open_obj)
            self.player_obj.house_action = ""
        elif self.player_obj.house_action == "close":
            self.remove_sprite(self.house_open_obj)
            self.player_obj.house_action = ""

        for sprite in self.all_sprites:
            if sprite.location == self.game.current_location:
                if sprite not in self.drawn_sprites:
                    self.load_sprite(sprite)
            elif sprite in self.drawn_sprites:
                self.remove_sprite(sprite)

        if self.game.current_location == [0, 0, 1]:
            self.bg = self.wood_bg
        if self.game.current_location == [0, -1, 1]:
            self.game.current_location = [0, 0]
            self.player_obj.rect.centerx = self.game.width / 2
            self.player_obj.rect.centery = self.game.height - 50
            self.reset_bg = True
        if self.game.current_location != [0, 0]:
            self.reset_bg = True
        elif self.reset_bg:
            self.bg = self.gras_bg
            self.reset_bg = False

        # pause menu
        if self.game.actions["escape"]:
            self.game.button_sprites.update()

            if self.game.start_but.clicked:
                self.game.actions["escape"] = False
            elif self.game.quit_but.clicked:
                self.game.running = False

    def render(self, win):
        win.blit(self.bg, (0, 0))

        self.drawn_sprites.draw(win)

        if self.game.actions["escape"]:
            win.blit(self.bg_blur, (0, 0))

            self.game.button_sprites.draw(win)

    def load_sprite(self, sprite):
        self.drawn_sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.drawn_sprites.remove(sprite)
