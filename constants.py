import pygame
from utils import render_font

pygame.font.init()
pygame.mixer.init()

SCREEN_NAMES = ['menu', 'hard_game', 'easy_game', 'how_to_play', 'high_scores']

TINY_FONT = pygame.font.Font('freesansbold.ttf', 17)
SMALL_FONT = pygame.font.Font('freesansbold.ttf', 18)
INTERMEDIATE_FONT = pygame.font.Font('freesansbold.ttf', 24)
MEDIUM_FONT = pygame.font.Font('freesansbold.ttf', 26)
BIG_FONT = pygame.font.Font('freesansbold.ttf', 34)


MENU_CONSTANTS = {
    'TITLE': render_font('The Meditating Ninja', font=BIG_FONT),
    'NAME': render_font('ENTER NAME: ', font=MEDIUM_FONT),
    'NAME_BOX': pygame.Surface([250, 40]),
    'WARNING': render_font('Type your name before playing.', font=SMALL_FONT),
    'NINJA_IMAGE': pygame.transform.scale(pygame.image.load('images/m_ninja.png'), [183, 198]),
}

MENU_CONSTANTS['NAME_BOX'].fill([255, 255, 255])


GAME_CONSTANTS = {
    'GATE_IMAGE': pygame.transform.scale(pygame.image.load('images/gate.png'), [396, 295]),
    'NINJA_IMAGE': pygame.transform.scale(pygame.image.load('images/m_ninja.png'), [110, 119]),
    'NINJA_SIZE': [110, 119],
    'NINJA_POSITION': [245, 281],

    'SHURIKEN_IMAGE': pygame.transform.scale(pygame.image.load('images/shuriken.png'), [30, 30]),
    'SHURIKEN_SIZE': [30, 30],
    'SHURIKEN_POSITION': ([335, 321], [235, 321]),  # RIGHT, LEFT
    'SHURIKEN_SPEED': 8,

    'ENEMY_NINJA_IMAGE': [pygame.transform.scale(pygame.image.load('images/redninja_right.png'), [82, 98]), pygame.transform.scale(pygame.image.load('images/redninja_left.png'), [82, 98])],
    'ENEMY_NINJA_SIZE': [82, 99],
    'ENEMY_NINJA_POSITION': ([650, 301], [-132, 301]),
    'ENEMY_NINJA_SPEED': 3,

    'PANEL_SHURIKEN_IMAGE': pygame.transform.scale(pygame.image.load('images/shuriken.png'), [35, 35]),

    'GONG_SOUND': pygame.mixer.Sound('sounds/gong.ogg'),
    'SHURIKEN_SOUND': pygame.mixer.Sound('sounds/shuriken.ogg'),
}


RULES_CONSTANTS = {
    'TITLE': MENU_CONSTANTS['TITLE'],
    'SUBTITLE': render_font('Rules', font=MEDIUM_FONT),
    'BACK': render_font('Press Q to go back.', font=MEDIUM_FONT),
    'RULE_1': render_font('1) Your objective is to meditate in order to get wiser.', font=SMALL_FONT),
    'RULE_2': render_font('2) You need to stop evil ninjas from disturbing the meditation.', font=SMALL_FONT),
    'RULE_3': render_font('3) You can stop evil ninjas by throwing a shuriken.', font=SMALL_FONT),
    'RULE_4': render_font('4) To throw a shuriken to your right press RIGHT ARROW.', font=SMALL_FONT),
    'RULE_5': render_font('5) To throw a shuriken to your left press LEFT ARROW.', font=SMALL_FONT),
    'RULE_6': render_font('6) You need to answer a math question to get a shuriken.', font=SMALL_FONT),
    'RULE_7': render_font('7) To answer, type a number on your keyboard & press RETURN.', font=SMALL_FONT),
    'RULE_8': render_font('8) You get one shuriken per correct answer.', font=SMALL_FONT),
    'RULE_9': render_font('9) You cannot skip a question.', font=SMALL_FONT),
    'RULE_10': render_font('10) If an evil ninja reaches you, the game is over.', font=SMALL_FONT),
    'RULE_11': render_font("11) Your score is the ninja's final IQ.", font=SMALL_FONT),
}


HIGH_SCORES_CONSTANTS = {
    'TITLE': MENU_CONSTANTS['TITLE'],
    'SUBTITLE': render_font('Top 10 High Scores', font=MEDIUM_FONT),
    'BACK': RULES_CONSTANTS['BACK'],
}
