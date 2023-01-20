import pygame as pg


class Player(pg.sprite.Sprite):
    def __init__(self, game, width, height, img_url, x, y):
        super().__init__()

        self.game = game

        self.house_action = ""

        self.sprite_sheet = pg.image.load(img_url)
        self.image = self.get_image(self.sprite_sheet, 2, 0, width, height, 2)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collide_offset = 5

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

    def update(self, furniture_sprites):
        keys = pg.key.get_pressed()

        """
        if keys[pg.K_SPACE] and not self.jumping:
            self.jumping = True
        """

        if keys[pg.K_w]:
            self.play_animation(2)
            self.check_move(self.collide_offset, self.collide_offset, self.collide_offset, 0, 1, -self.vel, furniture_sprites)

        elif keys[pg.K_s]:
            self.play_animation(0)
            self.check_move(self.collide_offset, self.collide_offset, 0, self.collide_offset, 1, self.vel, furniture_sprites)

        if keys[pg.K_a]:
            self.play_animation(1)
            self.check_move(self.collide_offset, 0, self.collide_offset, self.collide_offset, 0, -self.vel, furniture_sprites)

        elif keys[pg.K_d]:
            self.play_animation(3)
            self.check_move(0, self.collide_offset, self.collide_offset, self.collide_offset, 0, self.vel, furniture_sprites)

        """
        if self.jumping:
            self.rect.y -= self.jump_vel
            self.jump_vel -= 1

            if self.jump_vel <= -self.jump_height - 1:
                self.jumping = False
                self.jump_vel = self.jump_height
        """

        if self.rect.left > self.game.width:
            self.rect.right = 0
            self.game.current_location[0] += 1
        if self.rect.right < 0:
            self.rect.left = self.game.width
            self.game.current_location[0] -= 1
        if self.rect.top > self.game.height:
            self.rect.bottom = 0
            self.game.current_location[1] -= 1
        if self.rect.bottom < 0:
            self.rect.top = self.game.height
            self.game.current_location[1] += 1

        if self.game.current_location == [0, 0]:
            if -30 < self.rect.centerx - self.game.width / 2 < 30:
                if self.game.height / 2 < self.rect.centery < self.game.height / 2 + 100:
                    self.house_action = "open"
                    self.reset_house = True
                if self.game.height / 2 < self.rect.centery < self.game.height / 2 + 75:
                    self.game.current_location = [0, 0, 1]
                    self.house_action = "close"
            elif self.reset_house:
                self.house_action = "close"
                self.reset_house = False

                # right, left, top, bottom = right offset, left offset etc.
    def check_move(self, right, left, bottom, top, direction, distance, furniture_sprites):

        if self.game.current_location == [0, 0]:
            if (self.rect.right < self.game.house_collide_x_offset + right or self.rect.left > self.game.width -
                self.game.house_collide_x_offset - left) or (
                    self.rect.bottom < self.game.house_collide_y_offset + bottom or
                    self.rect.top > self.game.height - self.game.house_collide_y_offset - top) or \
                    (self.game.win.get_at(self.rect.topleft) == (0, 0, 0, 255) and self.game.win.get_at(
                        self.rect.topright) == (0, 0, 0, 255)):
                self.move(direction, distance)
        elif self.game.current_location == [0, 0, 1]:
            should_move = True
            for sprite in furniture_sprites:
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
