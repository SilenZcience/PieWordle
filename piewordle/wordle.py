import argparse
import random
import sys
import os
from datetime import datetime as dt

from piewordle.util.data import WordleData, COLOR_GREEN, COLOR_YELLOW, COLOR_RESET
from piewordle.util.data import ALPHABET
from piewordle.util.dictionary import words_en, words_de
from piewordle.util.thread import RepeatedTimer


WD = WordleData(os.get_terminal_size())


def println(*args, end='', **kwargs) -> None:
    print(*args, **kwargs, end=end, flush=True)

def print_guess(wordle: str, guess: str, guess_count: int, wordle_length: int) -> None:
    char_occurence = {letter: 0 for letter in set(wordle)}
    guess_ = list(guess)
    # color guess:
    for i in range(wordle_length):
        if guess_[i] not in wordle:
            continue
        if guess_[i] == wordle[i]:
            char_occurence[guess_[i]] += 1
            WD.guessed[guess_[i]] = f"{COLOR_GREEN}{guess_[i]}{COLOR_RESET}"
            guess_[i] = WD.guessed[guess_[i]]
    for i in range(wordle_length):
        if guess_[i] in wordle and guess_[i] != wordle[i]:
            char_occurence[guess_[i]] += 1
            if char_occurence[guess_[i]] <= wordle.count(guess_[i]):
                if WD.guessed[guess_[i]] == guess_[i]: # only make it yellow if it is not green
                    WD.guessed[guess_[i]] = f"{COLOR_YELLOW}{guess_[i]}{COLOR_RESET}"
                guess_[i] = f"{COLOR_YELLOW}{guess_[i]}{COLOR_RESET}"

    # move to position of guess_count's guess
    println(f"\x1b[{4+2*guess_count};{(WD.t_width-(2*wordle_length))//2 + 1}H")
    println(' '.join(guess_)) # print colored guess

def print_kb() -> None:
    println(f"\x1b[{WD.t_height-7};0H") # move to display keyboard line
    split_alphabet = [(0,10), (10,19), (19,26)]
    if WD.german_words: # append 'üöä' if in german keyboard
        split_alphabet.append((26,29))
    for f, t in split_alphabet:
        println(' '.join([WD.guessed[c] for c in ALPHABET[f:t]]), end='\n')

def reset_msg() -> None:
    println(f"\x1b[{WD.t_height-1};0H") # jump to line before last line
    println('\x1b[0K') # erase line

def print_msg(msg: str) -> None:
    reset_msg()
    println(msg) # display msg

def reset_prompt(wordle_length: int) -> None:
    println(f"\x1b[{WD.t_height-2};0H") # move to prompt line
    println('\x1b[0K') # erase line
    println('> ') # display prompt symbol
    println('\x1b[s') # save prompt position
    println('_' * wordle_length) # display empty prompt
    println('\x1b[u') # jump to saved position

def init(wordle_length: int) -> None:
    println('\x1b[2J\x1b[H') # clear screen and move to top left
    println('-' * ((WD.t_width-6)//2), 'WORDLE',
            '-' * ((WD.t_width-6)//2), sep='') # display header
    println(f"\x1b[{WD.t_height};0H") # move to bottom left
    println('-' * WD.t_width) # display bottom line
    x_offset = (WD.t_width-(2*wordle_length))//2 + 1
    for i in range(WD.allowed_guesses):
        println(f"\x1b[{4+2*i};{x_offset}H") # move to i'th guess position
        println(' '.join('☐' * wordle_length)) # print placeholder for guesses
    print_kb()
    reset_prompt(wordle_length)

def deinit(event: RepeatedTimer) -> None:
    println('\x1b[2J\x1b[H') # clear screen and move to top left
    event.cancel()

def retry() -> bool:
    reset_prompt(1)
    answer = input()[:1]
    return answer.upper() != 'N'

def get_wordle(daily: bool) -> str:
    if daily: # set a daily seed
        random.seed(int(dt.now().timestamp()//86400)) # 24*60*60 == 86400
    return random.choice(WD.words).upper()

def play_wordle(wordle: str) -> bool:
    wordle_length = len(wordle)
    init(wordle_length)

    input_buffer = ''
    guess_count = 0

    while guess_count < WD.allowed_guesses:
        if WD.screen_resized:
            # if the screen has been resized
            # rerender everything
            WD.screen_resized = False
            init(wordle_length)
            # including the old guesses
            for i, g in enumerate(WD.guess_history):
                print_guess(wordle, g, i, wordle_length)
        reset_prompt(wordle_length)
        println(input_buffer) # in case the resize interrupted the prompt
        guess = input() # main prompt
        if WD.screen_resized:
            # if the resize thread prompted to press enter
            # we buffer the input
            input_buffer = guess
            continue
        guess = input_buffer + guess # in case the buffer was not empty
        input_buffer = ''
        if len(guess) != wordle_length:
            print_msg(f"ERROR: The wordle has {wordle_length} letters!")
            continue
        if guess.lower() not in WD.words and not WD.allow_random:
            print_msg(f"ERROR: Unknown word: {guess}")
            continue
        guess = guess.upper()
        reset_msg() # we reset the errors, because the current guess is valid
        WD.guess_history.append(guess)
        print_guess(wordle, guess, guess_count, wordle_length)
        print_kb()
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
    if (width != WD.t_width or height != WD.t_height):
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
    argparser.add_argument('-?', action='store_const', default=False,
                           const=True, dest='Random',
                           help='allow not existing words.')
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
        WD.allowed_guesses > (WD.t_height-7)//2:
        print('Error: Invalid value for argument -g')
        print('the screen size might be too small to render')
        return 1
    WD.allow_random = getattr(parameters, 'Random')
    WD.german_words = getattr(parameters, 'DE')
    WD.words = words_de if WD.german_words else words_en
    words = getattr(parameters, 'Words')
    if words:
        WD.words = [word.lower() for word in words.split(';')]
        for wordle_option in WD.words:
            if not wordle_option.isalpha():
                print('Error: Invalid value for argument -w')
                return 2

    if 2*max(map(len, WD.words)) > WD.t_width-40:
        print('Error:')
        print('the screen size might be too small to render')
        return 3

    resize_event = RepeatedTimer(1, check_terminal_size)
    resize_event.start()

    try:
        while play_wordle(get_wordle(daily)):
            WD.reset()
    except (KeyboardInterrupt, EOFError):
        pass
    try:
        deinit(resize_event)
    except KeyboardInterrupt:
        resize_event.cancel()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
