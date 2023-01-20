import os
import pygame as pg
from button import Button
from states.title import Title
from states.game_world import Game_World


class Game:
    width, height = 960, 540
    win = pg.display.set_mode((width, height))
    pg.display.set_caption('RPG')

    clock = pg.time.Clock()
    running = True

    current_location = [0, 0]

    state_stack = []

    actions = {"start_game": False, "escape": False}

    house_collide_x_offset = (width - 315) / 2
    house_collide_y_offset = (height - 110) / 2

    cursor_arrow_img = pg.image.load(os.path.join('res', 'cursor_arrow.png'))
    cursor_hand_img = pg.image.load(os.path.join('res', 'cursor_hand.png'))

    active_cursor_img = cursor_arrow_img
    active_cursor_rect = active_cursor_img.get_rect()

    start_but = Button(100, 49 * 2, 0, "Start Game")
    select_save_but = Button(100, 49 * 4, 0, "Select Game Save")
    options_but = Button(100, 49 * 6, 0, "Options")
    quit_but = Button(100, 49 * 8, 13, "Quit Game")

    button_sprites = pg.sprite.Group(start_but, select_save_but, options_but, quit_but)

    def __init__(self):
        pg.init()

        self.load_states()

    def main(self):
        pg.mouse.set_visible(False)

        while self.running:
            self.clock.tick(60)
            self.get_events()
            self.update()
            self.render()

    def get_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE and not self.actions["escape"]:
                    self.actions["escape"] = True
                elif event.key == pg.K_ESCAPE:
                    self.actions["escape"] = False

    def update(self):
        self.state_stack[-1].update()

        # get mouse position and set custom cursor position
        self.active_cursor_rect.topleft = pg.mouse.get_pos()

    def render(self):
        self.state_stack[-1].render(self.win)

        # render custom cursor
        self.win.blit(self.active_cursor_img, self.active_cursor_rect)

        pg.display.flip()

    def generate_background(self, bg_img):
        background = pg.Surface((self.width, self.height))
        for y in range(0, self.height, bg_img.get_height()):
            for x in range(0, self.width, bg_img.get_width()):
                background.blit(bg_img, (x, y))
        return background

    def load_states(self):
        self.title_screen = Title(self)
        self.state_stack.append(self.title_screen)

    def draw_text(self, win, text, size, col, x, y):
        font = pg.font.Font(os.path.join("res", "fonts", "Oleaguid.ttf"), size)
        text_surf = font.render(text, True, pg.color.Color(col))
        win.blit(text_surf, (x - (text_surf.get_width() / 2), y - (text_surf.get_height() / 2)))


if __name__ == '__main__':
    g = Game()
    g.main()
    pg.quit()
    quit()
