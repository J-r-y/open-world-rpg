import pygame


class YAwareGroup(pygame.sprite.Group):
    # For setting the value
    def __setitem__(self, index, value):
        self.sprites()[index] = value
        print(self.sprites()[index], value)

    def by_y(self, spr):
        return spr.rect.centery

    def draw(self, surface):
        sprites = self.sprites()
        surface_blit = surface.blit
        for spr in sorted(sprites, key=self.by_y):
            self.spritedict[spr] = surface_blit(spr.image, spr.rect)
        self.lostsprites = []
