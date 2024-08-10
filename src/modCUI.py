import curses
import argparse
import readyGameForModding
import restoreBackToStock 
import randomizers.soundEffectRandomizer as soundEffectRandomizer
import randomizers.movieRandomizer as movieRandomizer
import randomizers.scriptRandomizer as scriptRandomizer
import randomizers.eventRandomizer as eventRandomizer
import time
import os

global randomizeSoundEffects
global randomizeVoices
randomizeSoundEffects = False
randomizeVoices = False

def submenu(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(100) # Set a timeout for getch

    # Initialize color pairs
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)

    submenu_options = ["Randomize Sound Effects (Some voices will still be randomized)", "Randomize Voices", "Start randomizer", "Back to Main Menu"]
    current_row = 0
    randomizeSoundEffects = False  # Assuming this is a global variable or passed in
    randomizeVoices = False  # Assuming this is a global variable or passed in

    while True:
        stdscr.clear()
        for idx, row in enumerate(submenu_options):
            if idx == 0:
                row = f"{row} [{'✔' if randomizeSoundEffects else '✘'}]"
            elif idx == 1:
                row = f"{row} [{'✔' if randomizeVoices else '✘'}]"
            x = 0  # Start from the leftmost position
            y = idx  # Start from the topmost position
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.attron(curses.color_pair(2))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(2))
        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(submenu_options) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                randomizeSoundEffects = not randomizeSoundEffects  # Toggle the value
            elif current_row == 1:
                randomizeVoices = not randomizeVoices  # Toggle the value
            elif current_row == 2:
                # Piece of shit code
                try: curses.endwin()
                except: break
                finally: 
                    soundEffectRandomizer.randomizeSoundEffects(args.path, randomizeSoundEffects, randomizeVoices)
                    time.sleep(2)
                    curses.wrapper(submenu)
                    break
            elif current_row == len(submenu_options) - 1:
                break

def optionThree():
    # WHY WHY WHY WHY WHY WHY WHY WHY WHY WHY WHY WHY WHY
    try: curses.wrapper(submenu)
    except: return
    finally: return
    

def run_option(option):
    # No point bothering without this try catch
    try: curses.endwin()
    except: curses.wrapper(main)
    finally:
        if option == 0:
            readyGameForModding.makeModdable(args.path)
            time.sleep(2)
        elif option == 1:
            restoreBackToStock.restore(args.path)
            time.sleep(2)
        elif option == 2:
            movieRandomizer.randomizeMovies(args.path)
            time.sleep(2)
        elif option == 3:
            scriptRandomizer.randomizeScripts(args.path)
            time.sleep(2)
        elif option == 4:
            eventRandomizer.randomizeEvents(args.path)
            time.sleep(2)
        elif option == 5:
            optionThree()
        curses.wrapper(main)

def main(stdscr):
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(1)   # Make getch non-blocking
    stdscr.timeout(100) # Set a timeout for getch

    # Menu options
    options = ["Make game moddable!", "Restore Game Back To Stock", "Randomize Movies", "Randomize Scripts", "Randomize Pictures", "Randomize Sound Effects"]
    current_option = 0

    while True:
        stdscr.clear()

        for idx, option in enumerate(options):
            if idx == current_option:
                stdscr.addstr(idx, 0, option, curses.A_REVERSE)  # Highlight selected option
            else:
                stdscr.addstr(idx, 0, option)

        stdscr.refresh()

        key = stdscr.getch()

        if key == curses.KEY_DOWN:
            current_option = (current_option + 1) % len(options)
        elif key == curses.KEY_UP:
            current_option = (current_option - 1) % len(options)
        elif key == 10:  # Enter key
            run_option(current_option)
        elif key == 27:  # Escape key to exit
            break


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deal with the game")
    parser.add_argument("path", help="Path to game files")
    args = parser.parse_args()

    if not os.path.isfile(args.path + "RouteProcSDHQ.dll"):
        print("Days game not detected!")
        exit(1)

    curses.wrapper(main)