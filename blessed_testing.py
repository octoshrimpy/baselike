import re
import sys
import time
import urwid
import random
import blessed

# show message in bottom line
def show_msg(term, msg = 'paused'):
    txt_paused = msg
    outp = term.move_yx(term.height - 1, int(term.width / 2 - len(txt_paused) / 2))
    outp += txt_paused
    print(outp, end='')
    sys.stdout.flush()

# such verbose, very words, many clean
def toggle_pause(term, pause):
    pause = not pause

    if pause == False:
        show_msg(term, '      ')
    
    return pause

# remove stupid ansi codes  from strings
def escape_ansi(line):
    ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', line)


def normalize_input(key):
        if type(key) is tuple:
            key = list(key)
            if key[0] == 'mouse press' or key[0] == 'mouse drag':
                if key[1] == 1.0:
                    key[1] = "left click"
                if key[1] == 2.0:
                    key[1] = "middle click"
                if key[1] == 3.0:
                    key[1] = "right click"
                if key[1] == 4.0:
                    key[1] = "scroll up"
                if key[1] == 5.0:
                    key[1] = "scroll down"
        
        return key


def handle_input(key):
    if ("mouse", "left",) in normalize_input(key):
        show_msg('lmouse')
        


# do the main thing
def rand_print(term, data):
    x = random.randint(0, term.width)
    y = random.randint(0, term.height)

    # get char
    ch = ''
    outp = term.move_xy(x, y)
    
    try:
        ch = data[f'{x}{y}']['char']
    except:
        data[f'{x}{y}'] = {"char": ''}

    # checks
    if ch == '-':
        chout = f'{term.orange}='

    elif ch == '=':
        chout = f'{term.orangered}#'

    elif ch == '#':
        y += 1
        outp = term.move_xy(x, y)
        chout = f'{term.teal}|'

    elif ch == '|':
        y += 1
        outp = term.move_xy(x, y)
        chout = f'{term.blue}║'
    
    else:
        chout = f'{term.yellow}-' 


    # save to data structure
    try:
        data[f'{x}{y}']['char'] = escape_ansi(chout)
    except:
        data[f'{x}{y}'] = {"char": escape_ansi(chout)}

    # set up output for writing
    outp += chout

    print(outp, end='')

    return data


def draw(term, data):
    pass


# main thing
def main(term):
    data = {}

    # setup term
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        pause = False

        # game loop
        while True:
            if pause:
                show_msg(term)

            # do things
            if not pause:
                data = rand_print(term, data)
                # data = draw(term, data)
                sys.stdout.flush()

            # inputs
            inp = term.inkey(timeout=0.01 if not pause else None)

            if inp in ('q', 'Q'):
                show_msg(term, 'quitting')
                time.sleep(1)
                exit()
            
            if inp == ' ':
                pause = toggle_pause(term, pause)


# if ran as main process
if __name__ == "__main__":
    loop = urwid.MainLoop(exit(main(blessed.Terminal())), unhandled_input=handle_input, screen=urwid.curses_display.Screen()) 
    loop.run()
    