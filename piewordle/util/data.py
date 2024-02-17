COLOR_RESET  = '\x1b[0m'
COLOR_YELLOW = '\x1b[3;33m'
COLOR_GREEN  = '\x1b[4;32m'

class WordleData:
    def __init__(self, terminal_size) -> None:
        self.t_width, self.t_height = terminal_size
        self.screen_resized = False
        self.allowed_guesses = 6
        self.words = []
        self.allow_random = False
        self.guess_history = []
