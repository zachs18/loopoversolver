# loopoversolver

Solver for https://www.openprocessing.org/sketch/580366

Requirements:

* Python3

* pyautogui (`pip install pyautogui` or `pip3 install pyautogui`)

* Fallback on Ubuntu (or probably other Linux distros) if pyautogui is not installed: xdotool (`sudo apt install xdotool`)

Note: If neither pyautogui nor xdotool is found, this project will output the keystrokes that would have been typed to stderr.

## Usage:

1. Open Loopover in a web browser, scramble, and *use the arrow keys to select the top-left cell*.

2. Run `python3 main.py` in a terminal

3. Type the board (space separated numbers or optinally space separated letters), newline terminates.

4. Alt-Tab back to the web browser before the 4 second timer runs out.

5. Wait.


