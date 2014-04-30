import pygame
import random
import sys

from pygame.locals import *


class game_sprites(pygame.sprite.Sprite):

    def __init__(self, size, colour, pos_x = None, pos_y = None, weight = 10, sprite_type= None):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface(size)
        self.image.fill(colour)

        if sprite_type is "char":
            self.invincible = True
            image_one = pygame.image.load("char_0.png")
            image_two = pygame.image.load("char_1.png")
            image_three = pygame.image.load("char_2.png")
            self.char_images = [image_one, image_two, image_three]
            self.image.blit(self.char_images[0], (0, 0))

        elif sprite_type is "ring":
            pygame.draw.circle(self.image, (255,215,0), (size[0]/2, size[1]/2), 11, 6)
            self.image.set_colorkey((255, 255, 255))

        self.size = size
        self.colour = colour

        self.rect = self.image.get_rect()
        if pos_x is not None:
            self.rect.x = pos_x
        if pos_y is not None:
            self.rect.y = pos_y

        self.falling = False

        self.weight = weight


class main_code:

    def main(self):
        # pygame setup
        pygame.font.init()
        size = width, height = 800, 600
        display = pygame.display.set_mode(size)
        fps_clock = pygame.time.Clock()

        # character created early for use with screen boundaries
        character = game_sprites((20, 30), (255, 255, 255), sprite_type="char")

        top_boundary = 50
        bottom_boundary = height - 25 - character.rect.height
        left_boundary = 0
        right_boundary = width - character.rect.width

        # graphics
        foreground_floor = game_sprites((width, 25), (0, 255, 0), pos_y=height- 25)
        background_wall = game_sprites((width, height - 25), (108, 81, 47))
        foreground_roof = game_sprites((800, 100), (28, 8, 0))

        # initial character position
        character.rect.x = left_boundary
        character.rect.y = bottom_boundary

        # create sprite groups
        player_group = pygame.sprite.Group()
        boulder_group = pygame.sprite.Group()
        coin_group = pygame.sprite.Group()
        background_group = pygame.sprite.Group()
        foreground_group = pygame.sprite.Group()

        # populate sprite groups
        player_group.add(character)
        background_group.add(background_wall)
        foreground_group.add(foreground_floor)
        foreground_group.add(foreground_roof)

        pygame.font.init()

        score = 0
        lives = 3
        coins = 0

        while 1:
            # check for death, restart TODO: change to choice
            if lives <= 0:
                boulder_group.empty()
                coin_group.empty()
                score = 0
                lives = 3
            # when 10 coins have been collected convert to life
            if coins >= 10:
                lives += 1
                coins = 0

            #score, lives, coins text for blitting
            font = pygame.font.Font(None, 26)
            score_text = font.render("Score: {}".format(score), 1, (255, 0, 0))
            life_text = font.render("Lives: {}".format(lives), 1, (255, 0, 0))
            coin_text = font.render("Coins: {}".format(coins), 1, (255, 0, 0))


            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            #character movement and basic animation
            key = pygame.key.get_pressed()
            if key[K_LEFT] and character.rect.x > left_boundary:
                character.rect.x -= 10
                character.invincible = False
                character.image =pygame.transform.scale(character.image, (character.size[0] / 2, character.size[1]))
                character.image.blit(character.char_images[1], (0, 0))
            if key[K_RIGHT] and character.rect.x < right_boundary:
                character.invincible = False
                character.rect.x += 10
                character.image.blit(character.char_images[2], (0, 0))
                character.image = pygame.transform.scale(character.image, (character.size[0] / 2, character.size[1]))
            if key[K_LEFT] == False and key[K_RIGHT] == False:
                character.image = pygame.transform.scale(character.image, (character.size[0], character.size[1]))
                character.image.blit(character.char_images[0], (0, 0))

            # choose whether a block should fall, gives some variation
            for block in boulder_group:
                if block.falling is False:
                    if random.choice([0, 1, 1, 1, 1]) == 0:
                        block.falling = True
                # move by block weight and kill if off screen
                else:
                    block.rect.y += block.weight
                    if block.rect.y > height:
                        block.kill()
            # create more boulders when there are only 10 left, increment score if player not invincible
            if len(boulder_group) < 10:
                for each in player_group:
                    if each.invincible is False:
                        score += 1
                # create boulders, width and height random to within 30 pixels and weight is half of size
                for i in range(10):
                    size = (random.randint(20, 50), random.randint(20, 50))
                    weight = size[0] / 2
                    new_block = game_sprites(size, (68, 41, 7), weight=weight)
                    new_block.rect.x = random.randint(left_boundary, right_boundary)
                    new_block.rect.y = top_boundary
                    boulder_group.add(new_block)

            # spawn coins
            if random.choice(range(0, 40)) == 1:
                coin = game_sprites((20, 20), (255, 255, 255), sprite_type="ring")
                coin.rect.x = random.randint(left_boundary, right_boundary)
                coin.rect.y = top_boundary
                coin_group.add(coin)

            for coin in coin_group:
                coin.rect.y += 10

            #check for collision with boulders
            collision_detect_boulder = pygame.sprite.groupcollide(player_group, boulder_group, False, False)
            for event in collision_detect_boulder:
                for each in player_group:
                    if each.invincible is not True:
                        character.rect.x = width / 2
                        each.invincible = True
                        score -= 5
                        lives -= 1

            #check for collision with coins
            collision_detect_coin = pygame.sprite.groupcollide(player_group, coin_group, False, True)
            for event in collision_detect_coin:
                coins += 1
                score += 10

            # draw game to screen
            display.fill((0, 0, 0))

            background_group.draw(display)
            coin_group.draw(display)
            boulder_group.draw(display)
            foreground_group.draw(display)
            player_group.draw(display)
            display.blit(score_text, (0, 0))
            display.blit(life_text, (width - 200, 0))
            display.blit(coin_text, ((width / 2) - 100, 0))

            pygame.display.flip()
            fps_clock.tick(30)


if __name__ == "__main__":
    main_code().main()