import pygame
from pygame.locals import *
import random
import copy
import math

BLOCK_SIZE = 30
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE1 = (255, 128, 0)
ORANGE2 = (255, 153, 51)
LIGHT_BLUE1 = (51, 255, 255)
LIGHT_BLUE2 = (153, 255, 255)
DARK_BLUE1 = (0, 0, 204)
DARK_BLUE2 = (51, 51, 255)
RED1 = (255, 0, 0)
RED2 = (255, 51, 51)
PURPLE1 = (68, 0, 102)
PURPLE2 = (136, 0, 204)
GREEN1 = (0, 200, 100)
GREEN2 = (0, 240, 100)
COLORS = [[ORANGE1, ORANGE2], [LIGHT_BLUE1, LIGHT_BLUE2], [DARK_BLUE1, DARK_BLUE2],
          [RED1, RED2], [PURPLE1, PURPLE2], [GREEN1, GREEN2]]

# Block Construction Guide
IBLOCK = [[BLOCK_SIZE, 0]]*3
BZBLOCK = [[BLOCK_SIZE, 0], [BLOCK_SIZE * -2, BLOCK_SIZE], [BLOCK_SIZE, 0]]
ZBLOCK = [[BLOCK_SIZE, 0], [0, BLOCK_SIZE], [BLOCK_SIZE, 0]]
SQUARE = [[BLOCK_SIZE, 0], [BLOCK_SIZE * -1, BLOCK_SIZE], [BLOCK_SIZE, 0]]
TBLOCK = [[BLOCK_SIZE, 0], [BLOCK_SIZE, 0], [BLOCK_SIZE * -1, BLOCK_SIZE]]
LBLOCK = [[BLOCK_SIZE, 0], [BLOCK_SIZE, 0], [0, BLOCK_SIZE]]
BLBLOCK = [[BLOCK_SIZE, 0], [BLOCK_SIZE, 0], [BLOCK_SIZE * -2, BLOCK_SIZE]]
RANDOM_BLOCK = [IBLOCK, ZBLOCK, BZBLOCK, SQUARE, TBLOCK, LBLOCK, BLBLOCK, IBLOCK]


class Tetrisgame:
    def __init__(self, w=300, h=750):
        # Initializes Window
        pygame.init()
        self.w = w
        self.h = h
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Tetris')
        # Initializes Block info
        self.start()
        self.music_start()
        self.font = pygame.font.Font('Resources/arial.ttf', 25)

    def average(self, list_):
        accumulator = 0
        for item in list_:
            accumulator += item
        return accumulator / len(list_)

    def remove_color(self, list_):
        colorless_blocks = []
        for block_with_color in list_:
            colorless_blocks.append(block_with_color[0:2])
        return colorless_blocks

    def illegal(self):
        # Loops through every moving block
        colorless_static_blocks = self.remove_color(self.static_block_cords)
        for mobile_block in self.mobile_block_cords:
            # Returns True if block is below the bounds
            if mobile_block:
                if mobile_block[1] + BLOCK_SIZE >= self.h:
                    return True
            # Returns True if block is too far Left
            if mobile_block[0] < 0:
                return True
            # Returns True if block is too far Right
            if mobile_block[0] > self.w - BLOCK_SIZE:
                return True
            # Returns True if block is in stationary Block
            modified_figure = [mobile_block[0], math.ceil(mobile_block[1] / BLOCK_SIZE) * BLOCK_SIZE]
            if modified_figure in colorless_static_blocks:
                return True
        return False

    def is_collision(self):
        # Gets only x and y values of blocks
        colorless_blocks = self.remove_color(self.static_block_cords)
        for block in self.mobile_block_cords:
            if block[1] + BLOCK_SIZE >= self.h:
                return True
            if [block[0], block[1] + BLOCK_SIZE] in colorless_blocks:
                return True
        return False

    def move_block(self):
        # If block is not colliding, move it down. Otherwise make it static and make new figure
        if not self.is_collision():
            for idx in range(4):
                self.mobile_block_cords[idx][1] += BLOCK_SIZE / 3
        else:
            for block in self.mobile_block_cords:
                self.static_block_cords.append(block)
            self.place_figure()

    def move_max_down(self):
        while not self.is_collision():
            for idx in range(4):
                self.mobile_block_cords[idx][1] += BLOCK_SIZE / 3

    def move_left(self):
        for idx in range(4):
            self.mobile_block_cords[idx][0] -= BLOCK_SIZE
        if self.illegal():
            for idx in range(4):
                self.mobile_block_cords[idx][0] += BLOCK_SIZE

    def move_right(self):
        for idx in range(4):
            self.mobile_block_cords[idx][0] += BLOCK_SIZE
        if self.illegal():
            for idx in range(4):
                self.mobile_block_cords[idx][0] -= BLOCK_SIZE

    def rotate_left(self):
        figure_copy = copy.deepcopy(self.mobile_block_cords)
        for idx in range(1, 4):
            x = self.mobile_block_cords[idx - 1][0] - figure_copy[idx - 1][1] + figure_copy[idx][1]
            y = self.mobile_block_cords[idx - 1][1] + figure_copy[idx - 1][0] - figure_copy[idx][0]
            self.mobile_block_cords[idx] = [x, y, self.mobile_block_cords[idx][2]]
        average_old_x = self.average([coord[0] for coord in figure_copy])
        average_old_y = self.average([coord[1] for coord in figure_copy])
        average_new_x = self.average([coord[0] for coord in self.mobile_block_cords])
        average_new_y = self.average([coord[1] for coord in self.mobile_block_cords])
        x_difference = round((average_old_x - average_new_x) / BLOCK_SIZE) * BLOCK_SIZE
        y_difference = round((average_old_y - average_new_y) / BLOCK_SIZE) * BLOCK_SIZE
        for idx, cord in enumerate(self.mobile_block_cords):
            self.mobile_block_cords[idx] = [cord[0] + x_difference, cord[1] + y_difference, cord[2]]
        if self.illegal():
            self.mobile_block_cords = copy.deepcopy(figure_copy)

    def rotate_right(self):
        figure_copy = copy.deepcopy(self.mobile_block_cords)
        for idx in range(1, 4):
            x = self.mobile_block_cords[idx - 1][0] + figure_copy[idx - 1][1] - figure_copy[idx][1]
            y = self.mobile_block_cords[idx - 1][1] - figure_copy[idx - 1][0] + figure_copy[idx][0]
            self.mobile_block_cords[idx] = [x, y, self.mobile_block_cords[idx][2]]
        average_old_x = self.average([coord[0] for coord in figure_copy])
        average_old_y = self.average([coord[1] for coord in figure_copy])
        average_new_x = self.average([coord[0] for coord in self.mobile_block_cords])
        average_new_y = self.average([coord[1] for coord in self.mobile_block_cords])
        x_difference = round((average_old_x - average_new_x) / BLOCK_SIZE) * BLOCK_SIZE
        y_difference = round((average_old_y - average_new_y) / BLOCK_SIZE) * BLOCK_SIZE
        for idx, cord in enumerate(self.mobile_block_cords):
            self.mobile_block_cords[idx] = [cord[0] + x_difference, cord[1] + y_difference, cord[2]]
        if self.illegal():
            self.mobile_block_cords = copy.deepcopy(figure_copy)

    def check_rows(self):
        dictionary = {}
        saved = []
        # Counts blocks per row
        for block in self.static_block_cords:
            dictionary[block[1]] = dictionary.get(block[1], 0) + 1
            if dictionary[block[1]] == 10:
                saved.append(block[1])
        # Removes all filled rows and moves rows above down
        if len(saved) > 0:
            self.score = self.score + 100 * 2 ** (len(saved) - 1)
            block_copy = copy.deepcopy(self.static_block_cords)
            for block in block_copy:
                if block[1] in saved:
                    self.static_block_cords.remove(block)
            for idx, block in enumerate(self.static_block_cords):
                if block[1] < min(saved):
                    self.static_block_cords[idx][1] = block[1] + BLOCK_SIZE * len(saved)

    def place_figure(self):
        last_block_x = BLOCK_SIZE * 4
        last_block_y = BLOCK_SIZE * -1
        color = COLORS[random.randint(0, 5)]
        self.mobile_block_cords = [[last_block_x, last_block_y, color]]
        block = RANDOM_BLOCK[random.randint(0, 7)]
        for instruction in block:
            last_block_x += instruction[0]
            last_block_y += instruction[1]
            self.mobile_block_cords.append([last_block_x, last_block_y, color])
        if self.illegal():
            self.game_over()

    def game_over(self):
        self.running = False

    def render_game_over(self):
        self.screen.fill(BLACK)
        text1 = self.font.render('GAME OVER', True, WHITE)
        text2 = self.font.render('Your Score Was ' + str(self.score), True, WHITE)
        text3 = self.font.render('Press Enter To Play Again', True, WHITE)
        self.screen.blit(text1, [70, 0])
        self.screen.blit(text2, [50, 30])
        self.screen.blit(text3, [0, 60])
        pygame.display.flip()

    def music_start(self):
        pygame.mixer.init()
    #     Load in files

    def render(self):
        self.screen.fill(BLACK)
        for idx in range(4):
            pygame.draw.rect(self.screen, self.mobile_block_cords[idx][2][0],
                             pygame.Rect(self.mobile_block_cords[idx][0], self.mobile_block_cords[idx][1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, self.mobile_block_cords[idx][2][1],
                             pygame.Rect(self.mobile_block_cords[idx][0] + 2, self.mobile_block_cords[idx][1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
        for idx in range(len(self.static_block_cords)):
            pygame.draw.rect(self.screen, self.static_block_cords[idx][2][0],
                             pygame.Rect(self.static_block_cords[idx][0], self.static_block_cords[idx][1], BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.screen, self.static_block_cords[idx][2][1],
                             pygame.Rect(self.static_block_cords[idx][0] + 2, self.static_block_cords[idx][1] + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))
        text = self.font.render('Score: ' + str(self.score), True, WHITE)
        self.screen.blit(text, [0, 0])
        pygame.display.flip()

    def start(self):
        self.running = True
        self.mobile_block_cords = []
        self.static_block_cords = []
        self.place_figure()
        self.score = 0

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                    if event.key == K_LEFT:
                        self.move_left()
                    if event.key == K_RIGHT:
                        self.move_right()
                    if event.key == K_DOWN:
                        self.move_max_down()
                    if event.key == K_a:
                        self.rotate_left()
                    if event.key == K_d:
                        self.rotate_right()
                elif event.type == QUIT:
                    quit()

            self.move_block()
            self.render()
            self.check_rows()
            self.clock.tick(20)
        while not self.running:
            self.render_game_over()
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        quit()
                    if event.key == K_RETURN:
                        self.start()
                        self.run()
                elif event.type == QUIT:
                    quit()


if __name__ == '__main__':
    tetris = Tetrisgame()
    tetris.run()
