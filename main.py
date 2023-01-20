import os
import pygame as pg
from button import Button
from YAwareGroup import YAwareGroup
from states.title import Title


class Obj(pg.sprite.Sprite):
    def __init__(self, size, img_url, scale, x, y, location):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface((size[0] * scale, size[1] * scale), pg.SRCALPHA)  # pg.SRCALPHA for transparency
        self.rect = self.image.get_rect()
        self.image.blit(pg.transform.scale_by(pg.image.load(img_url), scale), self.rect)
        self.rect.center = (x, y)

        self.location = location

    def update(self):
        if self.location == Game.current_location:
            if self not in Game.drawn_sprites:
                Game.load_sprite(g, self)
        elif self in Game.drawn_sprites:
            Game.remove_sprite(g, self)


class Player(pg.sprite.Sprite):
    def __init__(self, width, height, img_url, x, y):
        pg.sprite.Sprite.__init__(self)

        self.sprite_sheet = pg.image.load(img_url)
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

        if self.rect.left > Game.width:
            self.rect.right = 0
            Game.current_location[0] += 1
        if self.rect.right < 0:
            self.rect.left = Game.width
            Game.current_location[0] -= 1
        if self.rect.top > Game.height:
            self.rect.bottom = 0
            Game.current_location[1] -= 1
        if self.rect.bottom < 0:
            self.rect.top = Game.height
            Game.current_location[1] += 1

        if Game.current_location == [0, 0]:
            if -30 < self.rect.centerx - Game.width / 2 < 30:
                if Game.height / 2 < self.rect.centery < Game.height / 2 + 100:
                    Game.remove_sprite(g, Game.house_obj)
                    Game.load_sprite(g, Game.house_open_obj)
                    self.reset_house = True
                if Game.height / 2 < self.rect.centery < Game.height / 2 + 75:
                    Game.current_location = [0, 0, 1]
                    Game.remove_sprite(g, Game.house_open_obj)
            elif self.reset_house:
                Game.remove_sprite(g, Game.house_open_obj)
                Game.load_sprite(g, Game.house_obj)
                self.reset_house = False

    def check_move(self, right, left, bottom, top, direction,
                   distance):  # right, left, top, bottom = right offset, left offset etc.
        if Game.current_location == [0, 0]:
            if (self.rect.right < Game.house_collide_x_offset + right or self.rect.left > Game.width -
                Game.house_collide_x_offset - left) or (self.rect.bottom < Game.house_collide_y_offset + bottom or
                                                        self.rect.top > Game.height - Game.house_collide_y_offset - top) or \
                    (Game.win.get_at(self.rect.topleft) == (0, 0, 0, 255) and Game.win.get_at(self.rect.topright) == (
                            0, 0, 0, 255)):
                self.move(direction, distance)
        elif Game.current_location == [0, 0, 1]:
            should_move = True
            for sprite in Game.furniture_sprites:
                if not ((self.rect.right < sprite.rect.left + (right + 5) or self.rect.left > sprite.rect.right - (
                        left + 5))
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
        image = pg.transform.scale(image, (w * scale, h * scale))

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


class Game:
    width, height = 960, 540
    win = pg.display.set_mode((width, height))
    pg.display.set_caption('RPG')

    clock = pg.time.Clock()
    running = True
    reset_bg = False

    current_location = [0, 0]

    state_stack = []

    actions = {"start": False}

    house_collide_x_offset = (width - 315) / 2
    house_collide_y_offset = (height - 110) / 2

    cursor_arrow_img = pg.image.load(os.path.join('res', 'cursor_arrow.png'))
    cursor_hand_img = pg.image.load(os.path.join('res', 'cursor_hand.png'))

    active_cursor_img = cursor_arrow_img
    active_cursor_rect = active_cursor_img.get_rect()

    player_obj = Player(32, 32, os.path.join('res', 'dante.png'), width / 2, height - 50)
    house_obj = Obj((216, 216), os.path.join('res', 'house.png'), 1.5, width / 2, height / 2 - 50,
                    [0, 0])
    house_open_obj = Obj((216, 216), os.path.join('res', 'house_open.png'), 1.5, width / 2,
                         height / 2 - 50, [0, 0])

    schrank_obj = Obj((120, 128), os.path.join('res', 'schrank.png'), 1, 64, 66, [0, 0, 1])
    work_table_obj = Obj((160, 120), os.path.join('res', 'work_table.png'), 0.875, 210, 60, [0, 0, 1])
    bed_obj = Obj((32, 64), os.path.join('res', 'bed.png'), 2.5, width - 60, 100, [0, 0, 1])

    start_but = Button(100, 49 * 2, 0, "Start Game")
    select_save_but = Button(100, 49 * 4, 0, "Select Game Save")
    options_but = Button(100, 49 * 6, 0, "Options")
    quit_but = Button(100, 49 * 8, 13, "Quit Game")

    all_sprites = pg.sprite.Group(house_obj, player_obj, schrank_obj, work_table_obj,
                                  bed_obj)
    furniture_sprites = pg.sprite.Group(schrank_obj, work_table_obj, bed_obj)
    drawn_sprites = YAwareGroup(player_obj, house_obj)

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

    def update(self):

        self.state_stack[-1].update(self.actions)

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

    def load_sprite(self, sprite):
        self.drawn_sprites.add(sprite)

    def remove_sprite(self, sprite):
        self.drawn_sprites.remove(sprite)

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
