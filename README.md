# Checkers Game

This repository contains a simple command-line checkers game written in Python.

## Requirements

- Python 3

## Running the Game

Execute the game using Python:

```bash
python checkers.py
```

The board will be displayed in the terminal. Squares are labelled from `a` to `h` horizontally and `1` to `8` vertically. Black pieces are marked with `B` and white pieces with `W`. Kings are shown with a trailing `K`.

### Making Moves

When prompted, enter moves using the format `<from> <to>`. Both positions consist of a column letter (`a`-`h`) followed by a row number (`1`-`8`). For example:

```
a3 b4
```

The game alternates turns between black and white. Captures and kinging are supported following standard checkers rules.

Press `Ctrl+C` to quit the game at any time.

