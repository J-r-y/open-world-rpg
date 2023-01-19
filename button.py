import pygame as pg
import os

class Button(pg.sprite.Sprite):
    def __init__(self, x, y, type, text, function):
        super().__init__()

        self.x = x
        self.y = y
        self.text = text
        self.clicked = False
        self.function = function

        self.default_img = pg.transform.scale(pg.image.load(os.path.join('res', 'buttons', f'blue_button{type:02d}.png')), (220, 49))
        if type == 13:
            self.clicked_img = pg.transform.scale(pg.image.load(os.path.join('res', 'buttons', f'blue_button13.png')), (220, 49))
            self.draw_text("grey20")
        else:
            self.clicked_img = pg.transform.scale(pg.image.load(os.path.join('res', 'buttons', f'blue_button{type+1:02d}.png')), (220, 49))
            self.draw_text("white")
        self.image = self.clicked_img
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y

    def update(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.image = self.default_img
            if pg.mouse.get_pressed(3)[0]:
                self.image = self.clicked_img
                self.clicked = True
            else:
                self.image = self.default_img
                self.clicked = False
        else:
            self.image = self.clicked_img

    def draw_text(self, col):
        font = pg.font.Font(os.path.join("res", "fonts", "Oleaguid.ttf"), 30)
        text_surf = font.render(self.text, True, pg.color.Color(col))
        self.default_img.blit(text_surf, (110 - text_surf.get_rect().width / 2 + 2, 49 / 2 - text_surf.get_rect().height / 2 - 5))
        self.clicked_img.blit(text_surf, (110 - text_surf.get_rect().width / 2 + 2, 49 / 2 - text_surf.get_rect().height / 2))


class QuitButton(Button):
    def __init__(self, x, y, type, text, function):
        super().__init__(x, y, type, text, function)

        self.quit = False

    def update(self):
        super().update()

        if self.clicked:
            self.quit = True
