import pygame as pg


class Obj(pg.sprite.Sprite):
    def __init__(self, game, size, img_url, scale, x, y, location):
        pg.sprite.Sprite.__init__(self)

        self.game = game

        self.image = pg.Surface((size[0] * scale, size[1] * scale), pg.SRCALPHA)  # pg.SRCALPHA for transparency
        self.rect = self.image.get_rect()
        self.image.blit(pg.transform.scale_by(pg.image.load(img_url), scale), self.rect)
        self.rect.center = (x, y)

        self.location = location
