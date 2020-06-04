import pygame
import math
import random
import time
from constants import INTERMEDIATE_FONT, GAME_CONSTANTS
from utils import render_font


class Question:
    '''
    Defines a math question object. The question is random and can be updated in the same object.
    '''

    def __init__(self, is_easy):
        '''
        Initializes two numbers at random, picks up an operation,
        stores the result, and stores the operation symbol string.

        Args:
            is_easy (bool): whether the game difficulty is easy or not
        '''

        self.is_easy = is_easy

        if self.is_easy:  # If the game is easy only times tables allowed
            self.A = random.randint(0, 9)
            self.B = random.randint(1, 9)

            self.__operation = lambda a, b: (a * b, 'x')

        else:  # Hard game should have all operations and bigger numbers
            self.A = random.randint(0, 12)
            self.B = random.randint(1, 12)

            # Randomly selects a function which will return the answer and operation symbol
            self.__operation = random.choice([
                lambda a, b: (a + b, '+'),
                lambda a, b: (a - b, '-'),
                lambda a, b: (a * b, 'x'),
                lambda a, b: (a / b, '/')
            ])

        self.answer, self.operation_symbol = self.__operation(self.A, self.B)

        self.prevent_non_exact_division()

    def prevent_non_exact_division(self):
        '''Keeps picking new numbers if a division is not exact and updates attributes'''
        if self.operation_symbol != '/':
            return

        while (self.A % self.B != 0):
            self.A = random.randint(0, 12)
            self.B = random.randint(1, 12)

        self.answer, _ = self.__operation(self.A, self.B)

    def new_question(self):
        '''Re-runs the constructor to get a new random question'''
        self.__init__(is_easy=self.is_easy)

    def try_answer(self, answer):
        '''
        Checks if an answer is right or not

        Args:
            answer (int): answer to the math question

        Returns: boolean representing if the answer is right or not
        '''
        return int(answer) == self.answer

    def get_string(self):
        '''Returns: string representation of the math question'''
        return f'{self.A} {self.operation_symbol} {self.B} ='


class MeditatingNinja:
    '''Defines the meditating ninja which will appear in the game'''

    def __init__(self):
        '''Initializes the ninja's image, size, and positions on screen'''
        self.shape = GAME_CONSTANTS['NINJA_IMAGE']

        self.size = GAME_CONSTANTS['NINJA_SIZE']

        self.position = GAME_CONSTANTS['NINJA_POSITION']

    def render(self, display):
        '''Renders the meditating ninja on a given pygame display'''
        display.blit(self.shape, self.position)


class Shuriken:
    '''Defines a shuriken which will appear in the game'''

    def __init__(self, direction):
        '''
        Initializes shuriken direction, image, size, speed, and position depending on direction

        Args:
            direction (string): direction to which the shuriken will move, must be: "RIGHT" or "LEFT"
        '''
        self.direction = direction

        self.shape = GAME_CONSTANTS['SHURIKEN_IMAGE']

        self.size = GAME_CONSTANTS['SHURIKEN_SIZE']

        self.speed = GAME_CONSTANTS['SHURIKEN_SPEED']

        init_position = GAME_CONSTANTS['SHURIKEN_POSITION']
        self.position = init_position[0] if direction == 'RIGHT' else init_position[1]

    def render(self, display):
        '''Renders the shuriken on a given pygame display'''
        display.blit(self.shape, self.position)

    def update_position(self):
        '''
        In each frame the shuriken will move its speed in pixels to its direction.
        Adding to the x-coordinate means going to the right of the screen.
        Subtracting from the x-coordinate means going to the left of the screen.
        '''
        if self.direction == 'RIGHT':
            self.position = self.position[0] + self.speed, self.position[1]

        if self.direction == 'LEFT':
            self.position = self.position[0] - self.speed, self.position[1]


class EnemyNinja:
    '''Defines an enemy ninja which will appear in the game'''

    def __init__(self, side):
        '''
        Initializes the ninja's side (where he comes from on the screen), shape
        (images that varies depending on the side), size, speed, position (varies
        depending on the side).

        Args:
            side (string): side which the enemy ninjas comes from, must be: "RIGHT" or "LEFT"
        '''
        self.side = side

        if side == 'RIGHT':
            self.shape = GAME_CONSTANTS['ENEMY_NINJA_IMAGE'][0].convert_alpha()
        else:
            self.shape = GAME_CONSTANTS['ENEMY_NINJA_IMAGE'][1].convert_alpha()

        self.size = GAME_CONSTANTS['ENEMY_NINJA_SIZE']

        self.speed = GAME_CONSTANTS['ENEMY_NINJA_SPEED']

        init_position = GAME_CONSTANTS['ENEMY_NINJA_POSITION']
        self.position = init_position[0] if side == 'RIGHT' else init_position[1]

    def render(self, display):
        '''Renders an enemy ninjas on a given pygame display'''
        display.blit(self.shape, self.position)

    def update_position(self):
        '''
        In each frame the enemy ninja will move its speed in pixels towards 
        the center of the screen.
        Adding to the x-coordinate means going to the right direction.
        Subtracting from the x-coordinate means going to the left direction.
        '''
        if self.side == 'RIGHT':
            self.position = self.position[0] - self.speed, self.position[1]

        if self.side == 'LEFT':
            self.position = self.position[0] + self.speed, self.position[1]


class Panel:
    '''
    Defines the panel shown on the top of the game screen.
    It mainly deals with displaying information for the user.
    '''

    def __init__(self, is_easy):
        '''
        Initializes all attributes which will be shown on screen:
        math question , player score, shuriken count.
        '''
        self.is_easy = is_easy

        self.math_question = Question(is_easy)

        self.math_question_text = render_font(
            self.math_question.get_string(), font=INTERMEDIATE_FONT
        )

        self.keyboard_input = ''

        self.keyboard_input_text = render_font(
            self.keyboard_input, font=INTERMEDIATE_FONT
        )

        self.text_box = pygame.Surface([100, 40])
        self.text_box.fill([200, 200, 200])

        self.score = 75

        self.score_text = render_font(
            f'Ninja IQ: {self.score}', font=INTERMEDIATE_FONT
        )

        self.shuriken_count = 0

        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )

    def render(self, display):
        '''Renders the whole panel on a given display'''
        self.render_math_question(display)
        self.render_score(display)
        self.render_shuriken_count(display)

    def render_math_question(self, display):
        '''Renders the math question on a given display'''
        display.blit(self.math_question_text, [10, 10])
        display.blit(self.text_box, [10, 40])
        display.blit(self.keyboard_input_text, [13, 43])

    def render_score(self, display):
        '''Renders the score on a given display'''
        display.blit(self.score_text, [225, 20])

    def render_shuriken_count(self, display):
        '''Renders the shuriken count on a given display'''
        display.blit(GAME_CONSTANTS['PANEL_SHURIKEN_IMAGE'], [470, 15])
        display.blit(self.shuriken_count_text, [510, 20])

    def add_score(self):
        '''Updates player score depending on game difficulty'''
        if self.is_easy:
            self.score += 5
        else:
            self.score += 10

        self.score_text = render_font(
            f'Ninja IQ: {self.score}', font=INTERMEDIATE_FONT
        )

    def spend_shuriken(self):
        '''Updates shuriken count when player throws a shuriken'''
        self.shuriken_count -= 1

        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )

    def process_keyboard(self, key):
        '''Processed keyboard input (player typing answer)'''
        key_pressed = pygame.key.name(key)

        if key_pressed in '0123456789':
            self.keyboard_input += key_pressed

        else:
            if key == pygame.K_MINUS:
                self.keyboard_input += '-' if len(
                    self.keyboard_input) == 0 else ''

            if key == pygame.K_RETURN:
                if len(self.keyboard_input) <= 0 or self.keyboard_input == '-':
                    return

                if self.math_question.try_answer(self.keyboard_input):
                    self.shuriken_count += 1
                    self.math_question.new_question()

                self.keyboard_input = ''

            if key == pygame.K_BACKSPACE:
                self.keyboard_input = self.keyboard_input[:-1]

        self.math_question_text = render_font(
            self.math_question.get_string(), font=INTERMEDIATE_FONT
        )
        self.keyboard_input_text = render_font(
            self.keyboard_input, font=INTERMEDIATE_FONT
        )
        self.shuriken_count_text = render_font(
            str(self.shuriken_count), font=INTERMEDIATE_FONT
        )


class ShurikenController:
    ''' 
    Defines a controller to deal with all shurikens appearing on screen.
    It is responsible for rendering and processing shuriken throws.
    '''

    def __init__(self, panel):
        ''' 
        Initializes an array to store all shurikens appearing
        on screen, and a panel attribute to modify the panel which
        appears at the top of the game screen. 

        Args:
            panel (Panel): panel to be updated  '''

        self.rendered_shurikens = []

        self.panel = panel

    def render(self, display):
        '''Renders every shuriken on a given display and updates their positions'''
        for shuriken in self.rendered_shurikens:
            shuriken.render(display)
            shuriken.update_position()

    def process_keyboard(self, key):
        '''Processes keystrokes in order to throw shurikens'''
        if self.panel.shuriken_count <= 0:
            return

        if key == pygame.K_LEFT:
            self.rendered_shurikens.append(Shuriken(direction='LEFT'))
            self.panel.spend_shuriken()

            pygame.mixer.Sound.play(GAME_CONSTANTS['SHURIKEN_SOUND'])

        if key == pygame.K_RIGHT:
            self.rendered_shurikens.append(Shuriken(direction='RIGHT'))
            self.panel.spend_shuriken()

            pygame.mixer.Sound.play(GAME_CONSTANTS['SHURIKEN_SOUND'])


class EnemyNinjaController:
    ''' 
    Defines a controller to deal with all enemy ninjas appearing on screen.
    It is responsible for rendering and spawning enemy ninjas.
    '''

    def __init__(self, spawn_time):
        '''
        Initializes an array to store all enemy ninjas appearing on 
        screen. A pygame event is set to be triggered between equal
        intervals of time in milliseconds (spawn_time). This event 
        is handled in the main loop of the game, calling spawn_enemy_ninjas.
        '''
        self.rendered_enemy_ninjas = []

        pygame.time.set_timer(pygame.USEREVENT, spawn_time)

    def render(self, display):
        '''Renders every enemy ninja on a given display and updates their positions'''
        for enemy_ninja in self.rendered_enemy_ninjas:
            enemy_ninja.render(display)
            enemy_ninja.update_position()

    def spawn_enemy_ninjas(self):
        '''Randomly choose a side for the ninja and adds it to the array.'''
        side = random.choice(['RIGHT', 'LEFT'])
        self.rendered_enemy_ninjas.append(EnemyNinja(side=side))


class CollisionController:
    '''
    Defines a controller for all collisions that may happen in the game.
    Depending on which agents collided a different action is taken.
    '''

    def __init__(self, meditating_ninja, shuriken_control, enemy_ninja_control, panel, gameover_action):
        '''Stores all game entities to access their properties within the class'''
        self.meditating_ninja = meditating_ninja
        self.shuriken_control = shuriken_control
        self.enemy_ninja_control = enemy_ninja_control
        self.panel = panel
        self.gameover_halt = gameover_action

    def __detect_collision(self, A, B):
        '''
        Function that detects the collision between two bodies.
        A collision is detected when the x-coordinate of a body
        is between the sides of the other. y-coordinates are not
        considered because there is no need for that in the game.

        Args: Two bodies with an x-y position property (in form of a list)

        Returns: bool representing wheter the bodies have collided 
        '''
        A_middle_x = A.position[0] + (A.size[0] // 2)

        B_front_x = B.position[0]
        B_back_x = B.position[0] + B.size[0]

        if A_middle_x >= B_front_x and A_middle_x <= B_back_x:
            return True

        return False

    def detect_gameover(self):
        '''
        Checks for collisions between all enemies and the meditating ninja.
        If a collision has happened a game over procedure is called.
        '''
        for enemy_ninja in self.enemy_ninja_control.rendered_enemy_ninjas:
            if self.__detect_collision(enemy_ninja, self.meditating_ninja):
                self.on_gameover_detected()

    def on_gameover_detected(self):
        '''
        Stops the game music and plays a sound effect. Freezes
        the screen and calls a procedure to halt game execution.
        '''
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(GAME_CONSTANTS['GONG_SOUND'])

        time.sleep(2)

        self.gameover_halt()

    def detect_player_scored(self):
        '''
        Checks for collisions between all shurikens and all enemy ninjas.
        If a collisions has happened a procedure is called to increase score.
        '''
        for shuriken in self.shuriken_control.rendered_shurikens:
            for enemy_ninja in self.enemy_ninja_control.rendered_enemy_ninjas:
                if self.__detect_collision(shuriken, enemy_ninja):
                    self.on_score(shuriken, enemy_ninja)

    def on_score(self, shuriken, enemy_ninja):
        '''Removes the enemy ninja and the shuriken which colliided from the screen, and increases score'''
        self.enemy_ninja_control.rendered_enemy_ninjas.remove(enemy_ninja)
        self.shuriken_control.rendered_shurikens.remove(shuriken)
        self.panel.add_score()

    def scan_for_collisions(self):
        '''Checks for all types of collisions'''
        self.detect_gameover()
        self.detect_player_scored()
