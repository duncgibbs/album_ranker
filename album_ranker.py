import sys
from os import path
from random import shuffle
import curses

def choose_list():
    file_choice = raw_input("Which list do you want to rank?\n1) Albums Released in 2016\n2) Albums Released in Other Years\nChoice: ")
    if file_choice == '1':
        return 'released_this_year'
    elif file_choice == '2':
        return 'released_different_year'
    else:
        print 'Not a valid choice.'
        sys.exit()

def get_albums_from_file(filename):
    file_path = path.dirname(path.realpath(__file__)) + '/' + filename + '.txt'
    file = open(file_path, 'r')
    albums = [line.strip('\n') for line in file.readlines()]
    shuffle(albums)
    return albums

filename = choose_list()
albums = get_albums_from_file(filename)
album_string_one = "\n".join(albums[:6])
album_string_two = "\n".join(albums[6:12])
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
screen.addstr(album_string_one + "\n\n" + album_string_two)
screen.move(6,0)
screen.insstr(' > ' + albums[-1], curses.color_pair(1))
screen.refresh()
screen.getch()
curses.endwin()

#while albums:
#    album = albums.pop()

