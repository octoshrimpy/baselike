import urwid
import curses

###################
# curses stuff


_screen = curses.initscr()

def printchar(x,y,char):
    _screen.addch(y, x, char)


###################


MODE = ''

def exit():
    raise urwid.ExitMainLoop()


def handle_input(key):
    global MODE

    if key in ('q', 'Q'):
        exit()

    # toggle paint mode
    elif key in ('p', 'P'):
        if MODE == 'paint':
            MODE =''
            txt.set_text('paint mode OFF')
        else: 
            MODE = 'paint'
            txt.set_text('paint mode ON')

    elif type(key) is tuple:
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

    # else:
        # txt.set_text(repr(key))     

    if MODE == 'paint':
        if key[0] == 'mouse press' or key[0] == 'mouse drag':
            if key[1] == 1.0:
                x, y = key[2], key[3]
            
                printchar(x, y, '#')
    


# create output
txt = urwid.Text(('Hello world'), align='center')
fill = urwid.Filler(txt)

# run
loop = urwid.MainLoop(fill, unhandled_input=handle_input, screen=urwid.curses_display.Screen())
loop.run()
