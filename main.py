import os
import pygame as pg
import pygame.transform
from YAwareGroup import YAwareGroup

pg.init()
width, height = 960, 540
win = pg.display.set_mode((width, height))
pg.display.set_caption('Platformer')

clock = pg.time.Clock()

current_location = [0, 0]

house_collide_x_offset = (width - 315) / 2
house_collide_y_offset = (height - 110) / 2


class Obj(pg.sprite.Sprite):
    def __init__(self, size, img, x, y, location):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(size, pg.SRCALPHA)  # pg.SRCALPHA for transparency
        self.rect = self.image.get_rect()
        self.image.blit(img, self.rect)
        self.rect.center = (x, y)

        self.location = location

    def update(self):
        if self.location == current_location:
            if self not in drawn_sprites:
                load_sprite(self)
        elif self in drawn_sprites:
            remove_sprite(self)


class Player(pg.sprite.Sprite):
    def __init__(self, width, height, img, x, y):
        pg.sprite.Sprite.__init__(self)

        self.sprite_sheet = img
        self.image = self.get_image(self.sprite_sheet, 2, 0, width, height, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collide_offset = width / 10

        self.animation_list = []
        for direction in range(4):  # 4 directions for walking animation
            self.animation_list.append(self.get_animation(direction))
        self.animation_step = 0
        self.animation_step_counter = 0

        self.reset_house = False

        self.jump_height = 15
        self.jump_vel = self.jump_height
        self.jumping = False

        self.vel = 5

    def update(self):
        global current_location
        keys = pg.key.get_pressed()

        if keys[pg.K_SPACE] and not self.jumping:
            self.jumping = True

        if keys[pg.K_w]:
            self.play_animation(2)
            self.check_move(self.collide_offset, self.collide_offset, self.collide_offset, 0, 1, -self.vel)

        elif keys[pg.K_s]:
            self.play_animation(0)
            self.check_move(self.collide_offset, self.collide_offset, 0, self.collide_offset, 1, self.vel)

        if keys[pg.K_a]:
            self.play_animation(1)
            self.check_move(self.collide_offset, 0, self.collide_offset, self.collide_offset, 0, -self.vel)

        elif keys[pg.K_d]:
            self.play_animation(3)
            self.check_move(0, self.collide_offset, self.collide_offset, self.collide_offset, 0, self.vel)

        if keys[pg.K_x]:
            self.image = self.get_image(self.sprite_sheet, 1, 0, 32, 32, 2)

        if self.jumping:
            self.rect.y -= self.jump_vel
            self.jump_vel -= 1

            if self.jump_vel <= -self.jump_height - 1:
                self.jumping = False
                self.jump_vel = self.jump_height

        if self.rect.left > width:
            self.rect.right = 0
            current_location[0] += 1
        if self.rect.right < 0:
            self.rect.left = width
            current_location[0] -= 1
        if self.rect.top > height:
            self.rect.bottom = 0
            current_location[1] -= 1
        if self.rect.bottom < 0:
            self.rect.top = height
            current_location[1] += 1

        if current_location == [0, 0]:
            if -30 < self.rect.centerx - width / 2 < 30:
                if height / 2 < self.rect.centery < height / 2 + 100:
                    remove_sprite(house_obj)
                    load_sprite(house_open_obj)
                    self.reset_house = True
                if height / 2 < self.rect.centery < height / 2 + 75:
                    current_location = [0, 0, 1]
                    remove_sprite(house_open_obj)
            elif self.reset_house:
                remove_sprite(house_open_obj)
                load_sprite(house_obj)
                self.reset_house = False

    def check_move(self, right, left, bottom, top, direction, distance):  # right, left, top, bottom = right offset, left offset etc.
        if current_location == [0, 0]:
            if (self.rect.right < house_collide_x_offset + right or self.rect.left > width -
               house_collide_x_offset - left) or (self.rect.bottom < house_collide_y_offset + bottom or
               self.rect.top > height - house_collide_y_offset - top) or\
               (win.get_at(self.rect.topleft) == (0, 0, 0, 255) and win.get_at(self.rect.topright) == (0, 0, 0, 255)):
                self.move(direction, distance)
        elif current_location == [0, 0, 1]:
            should_move = True
            for sprite in furniture_sprites:
                if not ((self.rect.right < sprite.rect.left + (right + 5) or self.rect.left > sprite.rect.right - (left + 5)) 
                    or (self.rect.bottom < sprite.rect.top + bottom + sprite.rect.height / 1.51 or
                        self.rect.top > sprite.rect.bottom - top - (self.rect.height - 20))):
                    should_move = False
                    break
            if should_move:
                self.move(direction, distance)
        else:
            self.move(direction, distance)

    def move(self, direction, distance):  # direction 0 = x-axis, direction 1 = y-axis
        if direction == 0:
            self.rect.x += distance
        else:
            self.rect.y += distance

    def get_image(self, sheet, frame_x, frame_y, w, h, scale):
        image = pg.Surface((w, h), pg.SRCALPHA)
        image.blit(sheet, (0, 0), (frame_x * 48 + 8, frame_y * 48 + 11, w, h))
        image = pygame.transform.scale(image, (w * scale, h * scale))

        return image

    def get_animation(self, row):
        animation = []
        for y in range(4):
            animation.append(self.get_image(self.sprite_sheet, row, y, 32, 32, 2))

        return animation

    def play_animation(self, direction):
        self.image = self.animation_list[direction][self.animation_step]
        # self.animation_step = (self.animation_step + 1) % len(self.animation_list[direction])
        self.animation_step_counter += 1
        self.animation_step = self.animation_step_counter // 10
        if self.animation_step_counter > 36:
            self.animation_step_counter = 0


def generate_background(bg_img):
    background = pg.Surface((width, height))
    for y in range(0, height, bg_img.get_height()):
        for x in range(0, width, bg_img.get_width()):
            background.blit(bg_img, (x, y))
    return background

def load_sprite(sprite):
    drawn_sprites.add(sprite)

def remove_sprite(sprite):
    drawn_sprites.remove(sprite)


player_sprite_sheet_image = pg.image.load(os.path.join('res', 'dante.png'))
house_imgs = [pg.transform.scale(pg.image.load(os.path.join('res', 'house.png')), (216 * 1.5, 216 * 1.5)),
              pg.transform.scale(pg.image.load(os.path.join('res', 'house_open.png')), (216 * 1.5, 216 * 1.5))]

gras_bg = generate_background(pg.image.load(os.path.join('res', 'gras.png')))
wood_bg = generate_background(pg.image.load(os.path.join('res', 'plank.png')))

schrank_img = pg.image.load(os.path.join('res', 'schrank.png'))
work_table_img = pg.transform.scale(pg.image.load(os.path.join('res', 'work_table.png')), (140, 105))
bed_img = pg.transform.scale(pg.image.load(os.path.join('res', 'bed.png')), (64 * 1.25, 128 * 1.25))

bg = gras_bg

player_obj = Player(32, 32, player_sprite_sheet_image, width / 2, height - 50)
house_obj = Obj((216 * 1.5, 216 * 1.5), house_imgs[0], width / 2, height / 2 - 50, [0, 0])
house_open_obj = Obj((216 * 1.5, 216 * 1.5), house_imgs[1], width / 2, height / 2 - 50, [0, 0])

schrank_obj = Obj((120, 128), schrank_img, 64, 66, [0, 0, 1])
work_table_obj = Obj((140, 105), work_table_img, 210, 60, [0, 0, 1])
bed_obj = Obj((64 * 1.25, 128 * 1.25), bed_img, width - 60, 100, [0, 0, 1])

all_sprites = pg.sprite.Group(house_obj, player_obj, schrank_obj, work_table_obj, bed_obj)
furniture_sprites = pg.sprite.Group(schrank_obj, work_table_obj, bed_obj)
drawn_sprites = YAwareGroup(player_obj, house_obj)


def main():
    global bg, current_location
    running = True
    reset_bg = False
    while running:
        clock.tick(60)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
        if current_location == [0, 0, 1]:
            bg = wood_bg
        if current_location == [0, -1, 1]:
            current_location = [0, 0]
            player_obj.rect.centerx = width / 2
            player_obj.rect.centery = height - 50
            reset_bg = True
        if current_location != [0, 0]:
            reset_house = True
        elif reset_bg:
            bg = gras_bg
            reset_bg = False

        all_sprites.update()
        win.blit(bg, (0, 0))
        drawn_sprites.draw(win)

        pg.display.flip()


if __name__ == '__main__':
    main()
    pg.quit()
    quit()
