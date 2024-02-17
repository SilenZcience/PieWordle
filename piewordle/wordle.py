import argparse
import random
import sys
import os
from datetime import datetime as dt
from threading import Timer

from wordle.dictionary import words_en, words_de

COLOR_RESET  = '\x1b[0m'
COLOR_YELLOW = '\x1b[3;33m'
COLOR_GREEN  = '\x1b[4;32m'

class WordleData:
    def __init__(self) -> None:
        self.t_width, self.t_height = os.get_terminal_size()
        self.screen_resized = False
        self.allowed_guesses = 6
        self.words = words_en
        self.guess_history = []

WD = WordleData()

class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def cancel(self):
        self._timer.cancel()
        self._timer.join()
        self.is_running = False

def println(*args, **kwargs):
    print(*args, **kwargs, end='', flush=True)

def print_guess(wordle: str, guess: str, guess_count: int, wordle_length: int):
    char_occurence = {letter: 0 for letter in set(wordle)}
    guess_ = list(guess)
    for i in range(wordle_length):
        if guess_[i] not in wordle:
            continue
        if guess_[i] == wordle[i]:
            char_occurence[guess_[i]] += 1
            guess_[i] = f"{COLOR_GREEN}{guess_[i]}{COLOR_RESET}"
    for i in range(wordle_length):
        if guess_[i] in wordle and guess_[i] != wordle[i]:
            char_occurence[guess_[i]] += 1
            if char_occurence[guess_[i]] <= wordle.count(guess_[i]):
                guess_[i] = f"{COLOR_YELLOW}{guess_[i]}{COLOR_RESET}"

    # move to position of guess_count's guess
    println(f"\x1b[{4+2*guess_count};{(WD.t_width-(2*wordle_length))//2 + 1}H")
    println(' '.join(guess_)) # print colored guess

def reset_msg():
    println(f"\x1b[{WD.t_height-1};0H") # jump to line before last line
    println('\x1b[0K') # erase line

def print_msg(msg: str):
    reset_msg()
    println(msg) # display msg

def reset_prompt(wordle_length: int):
    println(f"\x1b[{WD.t_height-2};0H") # move to prompt line
    println('\x1b[0K') # erase line
    println('> ') # display prompt symbol
    println('\x1b[s') # save prompt position
    println('_' * wordle_length) # display empty prompt
    println('\x1b[u') # jump to saved position

def init(wordle_length: int):
    println('\x1b[2J\x1b[H') # clear screen and move to top left
    println('-' * ((WD.t_width-6)//2), 'WORDLE',
            '-' * ((WD.t_width-6)//2), sep='') # display header
    println(f"\x1b[{WD.t_height};0H") # move to bottom left
    println('-' * WD.t_width) # display bottom line
    x_offset = (WD.t_width-(2*wordle_length))//2 + 1
    for i in range(WD.allowed_guesses):
        println(f"\x1b[{4+2*i};{x_offset}H") # move to bottom left
        println(' '.join('☐' * wordle_length)) # print placeholder for guesses
    reset_prompt(wordle_length)

def deinit(event: RepeatedTimer):
    println('\x1b[2J\x1b[H') # clear screen and move to top left
    event.cancel()

def retry() -> bool:
    reset_prompt(1)
    answer = input()[:1]
    return answer.upper() != 'N'

def get_wordle(daily: bool) -> str:
    if daily:
        random.seed(int(dt.now().timestamp()//86400))
    return random.choice(WD.words).upper()

def play_wordle(wordle: str) -> bool:
    wordle_length = len(wordle)
    init(wordle_length)

    input_buffer = ''
    guess_count = 0

    while guess_count < WD.allowed_guesses:
        if WD.screen_resized:
            WD.screen_resized = False
            init(wordle_length)
            for i, g in enumerate(WD.guess_history):
                print_guess(wordle, g, i, wordle_length)
        reset_prompt(wordle_length)
        println(input_buffer)
        guess = input()
        if WD.screen_resized:
            input_buffer = guess
            continue
        guess = input_buffer + guess
        input_buffer = ''
        if len(guess) != wordle_length:
            print_msg(f"ERROR: The wordle has {wordle_length} letters!")
            continue
        if guess.lower() not in WD.words:
            print_msg(f"ERROR: Unknown word: {guess}")
            continue
        guess = guess.upper()
        reset_msg()
        WD.guess_history.append(guess)
        print_guess(wordle, guess, guess_count, wordle_length)
        if wordle == guess:
            print_msg(f"Congratulations: You found the Wordle: {wordle}! "
                      'Play again? [y]es/[n]o')
            return retry()
        guess_count += 1
    print_msg(f"Sadly you did not find the Wordle! The Wordle was: {wordle}. "
              'Play again? [y]es/[n]o')
    return retry()

def check_terminal_size() -> None:
    width, height = os.get_terminal_size()
    if not WD.screen_resized and \
        (width != WD.t_width or height != WD.t_height):
        WD.t_width, WD.t_height = width, height
        WD.screen_resized = True
        println('\x1b[2J\x1b[H') # clear screen and move to top left
        println('Screen Resize has been detected. Press Enter to rerender the screen.')

def main(argv) -> int:
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--daily', action='store_const', default=False,
                           const=True, dest='DAILY',
                           help='guess the daily wordle.')
    argparser.add_argument('-g', action='store', default=6,
                           metavar='GUESSES', dest='Guesses', type=int,
                           help='define the amount of guesses the player has. default is 6.')
    argparser.add_argument('--de', action='store_const', default=False,
                           const=True, dest='DE',
                           help='use german words.')
    argparser.add_argument('-w', action='store', default='',
                           metavar='WORDS', dest='Words', type=str,
                           help="define custom wordle options. Seperator is ';'.")

    parameters = argparser.parse_args(argv[1:])

    daily = getattr(parameters, 'DAILY')
    WD.allowed_guesses = getattr(parameters, 'Guesses')
    if WD.allowed_guesses <= 0 or \
        WD.allowed_guesses > (WD.t_height-8)//2:
        print('Error: Invalid value for argument -g')
        return 1
    if getattr(parameters, 'DE'):
        WD.words = words_de
    words = getattr(parameters, 'Words')
    if words:
        wordle_options = words.split(';')
        for wordle_option in wordle_options:
            if not wordle_option.isalpha():
                print('Error: Invalid value for argument -w')
                return 2
        WD.words = [wordle_option.lower() for wordle_option in wordle_options]

    resize_event = RepeatedTimer(1, check_terminal_size)
    resize_event.start()

    try:
        while play_wordle(get_wordle(daily)):
            WD.guess_history.clear()
    except (KeyboardInterrupt, EOFError):
        pass
    try:
        deinit(resize_event)
    except KeyboardInterrupt:
        resize_event.cancel()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
