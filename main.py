import pygame
from constants import SCREEN_NAMES
from menu import Menu
from game import HardGame, EasyGame
from rules import Rules
from high_scores import HighScores

pygame.init()

screens = dict(
    zip(SCREEN_NAMES, [Menu, EasyGame, HardGame, Rules, HighScores])
)


def open_window(screen, name=None):
    '''
    Function opens the screen given in the parameters, and initializes
    the screen with a name saved if there is any. When the screen is 
    closed, a new screen is opened if there is a next_screen set up.

    Args: 
        screen (string): name of the screen to be opened
        name (string): name of the player, optional.

    '''
    active_screen = screens[screen](name) if name else screens[screen]()

    while active_screen.run:
        active_screen.render_frame()

    try:
        open_window(active_screen.next_screen, name=active_screen.name)
    except KeyError:
        pygame.quit()


if __name__ == '__main__':
    # Loads and plays main menu music
    pygame.mixer.music.load('music/music_calm.wav')
    pygame.mixer.music.play(-1)

    open_window(SCREEN_NAMES[0])  # Opens screen zero (menu)
