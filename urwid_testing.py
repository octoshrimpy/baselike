import urwid

def exit():
    raise urwid.ExitMainLoop()


def handle_input(key):

    if key in ('q', 'Q'):
        exit()

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
            
    txt.set_text(repr(key))


# create output
txt = urwid.Text(('Hello world'), align='center')
fill = urwid.Filler(txt)

# run
loop = urwid.MainLoop(fill, unhandled_input=handle_input)
loop.run()
