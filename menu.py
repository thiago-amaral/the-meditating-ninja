import pygame
from utils import render_font, Screen
from constants import MEDIUM_FONT, SCREEN_NAMES, MENU_CONSTANTS
from string import ascii_lowercase


class Button():
    '''
    Defines a button which can be either active or inactive.
    Visuals vary depending on which state the button is in.
    '''

    def __init__(self, text, position):
        '''
        Initializes the button text, position, box (which will
        be the button's background), and which state the button
        is in (not active at first)

        Args:
            text (string): text which appear on the button
            position (list): position of the button on screen
        '''
        self.text = render_font(text, font=MEDIUM_FONT)
        self.position = position

        # pygame rectangle which appears as the button's background
        self.box = pygame.Surface([200, 40])
        self.box.fill([255, 255, 255])

        self.active = False

    def toggle_active(self):
        '''Inverts the active attribute (bool) and assigns the correct color'''
        self.active = not self.active

        if self.active:
            self.box.fill([150, 150, 150])
        else:
            self.box.fill([255, 255, 255])

    def render(self, display):
        '''Displays text and button background with a margin of 5px between them'''
        display.blit(self.box, (self.position[0] - 5, self.position[1] - 5))
        display.blit(self.text, self.position)


class Menu(Screen):
    '''
    Defines the main menu screen. Inherits screen methods from a
    parent class. Every frame of this screen is generated by running 
    the function render_frame once. All other methods deal with input 
    processing, except the constructor.
    '''

    def __init__(self, name=''):
        '''
        Saves ninja image attribute, adds all buttons to a list 
        attribute, and initializes the first button as active.

        Args:
            name (string): name of the player, optional.
        '''
        super().__init__(name)

        self.ninja_image = MENU_CONSTANTS['NINJA_IMAGE'].convert_alpha()

        self.buttons = []
        self.buttons.append(Button(text='PLAY [EASY]', position=[10, 180]))
        self.buttons.append(Button(text='PLAY [HARD]', position=[10, 240]))
        self.buttons.append(Button(text='RULES', position=[10, 300]))
        self.buttons.append(Button(text='HIGH SCORES', position=[10, 360]))

        self.active_button = 0
        self.buttons[self.active_button].toggle_active()

    def process_arrow_pressed(self, key):
        '''
        When the user presses arrow up or down, the active button changes.
        The function deactivates the old button, and activates the new one.
        '''
        if key == pygame.K_UP and self.active_button > 0:
            self.buttons[self.active_button].toggle_active()
            self.active_button -= 1  # Changes active to button below
            self.buttons[self.active_button].toggle_active()

        if key == pygame.K_DOWN and self.active_button < len(self.buttons) - 1:
            self.buttons[self.active_button].toggle_active()
            self.active_button += 1  # Changes active to button above
            self.buttons[self.active_button].toggle_active()

    def process_navigation_action(self, key):
        '''
        When the user presses return, a redirect is set which 
        will be used by the main code to change screens, and
        the menu stops running.
        '''
        if key == pygame.K_RETURN:
            next_screen = SCREEN_NAMES[self.active_button + 1]

            if len(self.name) < 1 and next_screen in ['hard_game', 'easy_game']:
                return

            self.set_next_screen(next_screen)
            self.stop_running()

    def process_typing_name(self, key):
        '''Changes the name attribute when a letter or the backspace key is pressed.'''
        if key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]

        if len(self.name) > 10:
            return

        key_name = pygame.key.name(key)

        if key_name in ascii_lowercase:
            self.name += key_name.upper()

    def render_frame(self):
        '''Renders one frame of the menu on a pygame display'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop_running()

            if event.type == pygame.KEYDOWN:
                self.process_arrow_pressed(event.key)
                self.process_typing_name(event.key)
                self.process_navigation_action(event.key)

        self.screen.fill([255, 184, 122])

        self.screen.blit(MENU_CONSTANTS['TITLE'], [10, 10])
        self.screen.blit(MENU_CONSTANTS['NAME'], [10, 80])
        self.screen.blit(MENU_CONSTANTS['NAME_BOX'], [220, 70])

        self.screen.blit(MEDIUM_FONT.render(
            self.name, True, [0, 0, 0]), [225, 80])

        self.screen.blit(MENU_CONSTANTS['WARNING'], [210, 115])
        self.screen.blit(self.ninja_image, [290, 202])

        for button in self.buttons:
            button.render(self.screen)

        pygame.display.update()