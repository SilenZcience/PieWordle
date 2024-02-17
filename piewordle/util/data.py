COLOR_RESET  = '\x1b[0m'
COLOR_YELLOW = '\x1b[3;33m'
COLOR_GREEN  = '\x1b[4;32m'

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
