import sys
import time
import random
import blessed


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


def rand_print(term):
    x = random.randint(0, term.width)
    y = random.randint(0, term.height)

    outp = term.move_yx(y, x)
    outp += '#'
    print(outp, end='')


def main(term):
    with term.fullscreen(), term.cbreak(), term.hidden_cursor():
        pause = False

        while True:
            if pause:
                show_msg(term)

            if not pause:
                
                # do things
                rand_print(term)
                
                sys.stdout.flush()

            # inputs
            inp = term.inkey(timeout=0.01 if not pause else None)

            if inp in ('q', 'Q'):
                show_msg(term, 'quitting')
                time.sleep(1)
                exit()
            
            if inp == ' ':
                pause = toggle_pause(term, pause)



# doesn't erase terminal history
if __name__ == "__main__":
    exit(main(blessed.Terminal()))