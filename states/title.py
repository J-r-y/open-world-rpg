import os
from states.state import State
from states.game_world import Game_World
import pygame as pg


class Title(State):
    def __init__(self, game):
        super().__init__(game)

        self.title_panel = pg.image.load(os.path.join('res', 'buttons', 'main_menu_panel.png'))
        self.title_panel_rect = self.title_panel.get_rect()
        self.title_panel_rect.right = self.game.width - 50
        self.title_panel_rect.centery = 75

    def update(self):
        self.game.button_sprites.update()

        if self.game.quit_but.clicked:
            self.game.running = False

        if self.game.start_but.clicked:
            self.game.actions["start_game"] = True

            new_state = Game_World(self.game)
            new_state.enter_state()

            self.game.actions["start_game"] = False

    def render(self, win):
        win.fill((125, 125, 125))

        win.blit(self.title_panel, self.title_panel_rect)
        self.game.draw_text(win, 'Best RPG', 50, 'grey20', self.game.width - 200, 75)

        self.game.button_sprites.draw(win)
