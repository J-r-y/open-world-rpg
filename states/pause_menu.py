from states.state import State
import pygame as pg


class Pause_Menu(State):
    def __init__(self, game):
        super().__init__(game)

        self.game = game




    def update(self, actions):
        if not self.game.actions["escape"]:
            self.exit_state()
