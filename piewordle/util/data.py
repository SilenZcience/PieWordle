
ALPHABET = 'QWERTZUIOPASDFGHJKLYXCVBNMÜÖÄ'

class WordleData:
    def __init__(self, terminal_size) -> None:
        self.t_width, self.t_height = terminal_size
        self.screen_resized = False

        self.allowed_guesses = 6
        self.words = []
        self.allow_random = False
        self.german_words = False

        self.guess_history = []
        self.guessed = {letter: letter for letter in ALPHABET}

    def reset(self) -> None:
        self.guess_history.clear()
        self.guessed = {letter: letter for letter in ALPHABET}

class ANSI:
    RESET  = '\x1b[0m'
    COLOR_DARK   = '\x1b[2m'
    COLOR_YELLOW = '\x1b[3;33m'
    COLOR_GREEN  = '\x1b[4;32m'

    UNDERLINE = '\x1b[4m'

    ERASE_SCREEN = '\x1b[2J'
    ERASE_LINE = '\x1b[0K'

    START_POS = '\x1b[H'
    SAVE_POS = '\x1b[s'
    RESET_POS = '\x1b[u'
    XY_POS = '\x1b[%d;%dH'
