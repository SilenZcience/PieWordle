import sys
from wordle.wordle import main

def entry_point():
    """entry_point"""
    sys.exit(main(sys.argv))

if __name__ == '__main__':
    entry_point()
