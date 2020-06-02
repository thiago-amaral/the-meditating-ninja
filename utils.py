import pygame


def render_font(text, font, color=[0, 0, 0]):
    '''
    Function that generates text ready to be displayed
    on screen by pygame.

    Args:
        text (string): the text to be rendered
        font (pygame.font.Font): font to render text
        color (list): RGB color of text

    Returns:
        pygame.Surface: text ready to be displayed on screen
    '''
    return font.render(text, True, color)


class Screen:
    '''
    Defines a Screen. It defines all methods 
    and attributes shared by all game screens.
    '''

    def __init__(self, name=''):
        '''
        Initializes a pygame window, initializes
        run property, declares next_screen, and
        stores player name if there is any.

        Args:
            name (string): name of the player, optional.
        '''

        pygame.display.set_caption('The Meditating Ninja')
        self.screen = pygame.display.set_mode([600, 400])

        self.run = True

        self.next_screen = None

        self.name = name

    def stop_running(self):
        '''Sets run attribute to false'''
        self.run = False

    def set_next_screen(self, screen_name):
        '''Sets next_screen attribute to a given name (string)'''
        self.next_screen = screen_name


class Ranking:
    '''
    Class defining a Ranking object. The object is connected to a 
    textfile. Consider line N (where N is odd) to be the name of 
    the player and line N + 1 the score of that player.
    '''

    def __init__(self, path):
        '''
        Reads a given textfile and initializes an attribute mapping
        each name to each score as a dictionary. Initializes an 
        attribute containing an ordered list of names, and the path
        to the textfile also becomes an attribute.

        Args:
            path (string): path to the textfile with names and scores.
        '''
        with open(path, 'r') as f:
            lines = f.read().splitlines()  # Stores each line in an array

        players = {}

        for i in range(0, len(lines) - 1, 2):  # Maps each name to each score
            players[lines[i]] = int(lines[i + 1])

        # Creates an ordered list of names based on the player's score.
        leaderboard = sorted(players, key=players.get, reverse=True)

        self.__players = players
        self.__leaderboard = leaderboard

        self.__path = path

    def update(self):
        '''Re-runs the constructor to update attributes with changes in textfile'''
        self.__init__(self.__path)

    def export_players(self):
        '''Re-writes textfile with players and scores stored in the object's attribute'''
        with open(self.__path, 'w') as f:
            for player in self.__players.keys():
                f.write(f'{player}\n')
                f.write(f'{self.__players[player]}\n')

    def new_record(self, name, score):
        '''
        Saves a new score to a dictionary (__players attribute) and 
        updates the textfile. If the player already has a score and 
        the new one is not their highest, the function does not run.

        Args:
            name (string): name of the player
            score (int): score of the player
        '''
        if name in self.__players and self.__players[name] > score:
            return

        self.__players[name] = score

        self.export_players()

        self.update()

    def get_leaderboard(self):
        '''Returns: dictionary that maps names to scores'''
        return self.__leaderboard

    def get_players(self):
        '''Returns: list of player names ordered by score'''
        return self.__players
