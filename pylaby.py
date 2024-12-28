import random
import sys
import tkinter
import time

DEBUG = 0

def debug(*msg):
    if DEBUG:
        print(msg)

def key_press(event):
    t = event.keysym
    if t == 'q': # "quit"
        debug('quit...')
        sys.exit(0)
    elif t == 'n': # "next"
        create_new_wall(canvas, laby_model)
    elif t == 's': # "stop"
        window.stop_wall = True


def draw_next_wall(count_left):
    if window.stop_wall:
        return
    if count_left <= 0:
        return
    create_new_wall(canvas, laby_model)
    window.after(50, draw_next_wall, count_left-1)


def draw_wall(canvas, row, column, value):
    if value == 0:
        return  # no wall
    # coordinates of the base point
    x = X0 + column*X_PACE
    y = Y0 + row*Y_PACE
    if value & 1:
        # wall below
        canvas.create_line(x, y, x, y + Y_PACE)
    if value & 2:
        # wall on the right
        canvas.create_line(x, y, x + X_PACE, y)


def display(canvas, laby_model):
    # draw the walls
    for row in range(len(laby_model)):
        for column in range(len(laby_model[row])):
            value = laby_model[row][column]
            draw_wall(canvas, row, column, value)


def randomize(laby_model):
    for row in range(len(laby_model)-2):
        for column in range(len(laby_model[row+1])-2):
            laby_model[row+1][column+1] = int(random.uniform(0, 4))
    return laby_model


def is_good_starting_point(laby_model, random_row, random_column):
    """Tell if a point has already a wall connected"""
    if laby_model[random_row][random_column] == 0:
        # look if a wall is coming from right
        if random_column > 0 and laby_model[random_row][random_column-1] & 2:
            return True
        # look if a wall is coming from above
        if random_row > 0 and laby_model[random_row-1][random_column] & 1:
            return True
        return False
    return True

def select_starting_point(laby_model):
    count = 0
    # Look for a valid starting point
    # - draw a random point
    # - if valid: ok
    # - if not valid, look for the nearest valid in a random direction
    random_row = int(random.uniform(0, len(laby_model)))
    random_column = int(random.uniform(0, len(laby_model[0])))
    is_good = is_good_starting_point(laby_model, random_row, random_column)
    debug("is_good=", is_good)
    if is_good:
        return (random_row, random_column)
    # else: draw a random direction
    direction = random.choice(['up', 'down', 'left', 'right'])
    debug("select_starting_point: direction=", direction)
    if direction == 'up':
        while random_row > 0:
            random_row -= 1
            is_good = is_good_starting_point(laby_model, random_row, random_column)
            if is_good:
                return (random_row, random_column)
        # not found. Should not be possible as the laby is surrounded by walls
    elif direction == 'down':
        while random_row < len(laby_model)-1:
            random_row += 1
            is_good = is_good_starting_point(laby_model, random_row, random_column)
            if is_good:
                return (random_row, random_column)
        # not found. Should not be possible as the laby is surrounded by walls
    elif direction == 'left':
        while random_column > 0:
            random_column -= 1
            is_good = is_good_starting_point(laby_model, random_row, random_column)
            if is_good:
                return (random_row, random_column)
        # not found. Should not be possible as the laby is surrounded by walls
    elif direction == 'left':
        while random_column < len(laby_model[0])-1:
            random_column += 1
            is_good = is_good_starting_point(laby_model, random_row, random_column)
            if is_good:
                return (random_row, random_column)
        # not found. Should not be possible as the laby is surrounded by walls

    return None


def is_possible_wall_right(laby_model, row, column):
    if laby_model[row][column] & 2:
        return False
    if column+1 >= len(laby_model[row]):
        return False
    if laby_model[row][column+1] != 0:
        return False
    # look if wall coming from above
    if row != 0:
        if laby_model[row-1][column+1] & 1:
            return False
    return True

def is_possible_wall_left(laby_model, row, column):
    if column == 0:
        return False
    # look if wall on left point
    if laby_model[row][column-1] != 0:
        return False
    # look if wall coming from up-left
    if row != 0 and laby_model[row-1][column-1] & 1:
        return False
    # look if wall coming from left-left
    if column >= 2 and laby_model[row][column-2] & 2:
        return False
    return True

def is_possible_wall_up(laby_model, row, column):
    if row == 0:
        return False
    # look if wall coming from up
    if laby_model[row-1][column] & 1:
        return False
    # look if wall coming from up-left
    if laby_model[row-1][column-1] & 2:
        return False
    # look if wall going from up to up-right
    if laby_model[row-1][column] & 2:
        return False
    # look if wall coming from up-up
    if row >= 2 and laby_model[row-2][column] & 1:
        return False
    return True

def is_possible_wall_down(laby_model, row, column):
    if laby_model[row][column] & 1:
        return False
    if row+1 >= len(laby_model):
        return False
    # look if wall strating from down
    if laby_model[row+1][column] != 0:
        return False
    # look if wall coming from down-left
    if column >= 1 and laby_model[row+1][column-1] & 2:
        return False
    return True

def create_random_wall(laby_model, row, column, canvas):
    # Get possible directions "up", "left", "right", "down"
    # right?

    n_walls = int(random.uniform(1, len(laby_model)*3))
    debug("n_walls=", n_walls)

    while n_walls >= 0:
        n_walls -= 1
        possibilities = []
        if is_possible_wall_right(laby_model, row, column):
            possibilities.append("right")
        if is_possible_wall_left(laby_model, row, column):
            possibilities.append("left")
        if is_possible_wall_up(laby_model, row, column):
            possibilities.append("up")
        if is_possible_wall_down(laby_model, row, column):
            possibilities.append("down")
    
        debug("possibilities=", possibilities)

        if len(possibilities) == 0:
            return False

        # Choose a possibiity of direction
        direction = possibilities[int(random.uniform(0, len(possibilities)))]
        debug("chosen=", direction)

        if direction == "right":
            laby_model[row][column] += 2
            column += 1
        if direction == "down":
            laby_model[row][column] += 1
            row += 1
        if direction == "up":
            laby_model[row-1][column] += 1
            row -= 1
        if direction == "left":
            laby_model[row][column-1] += 2
            column -= 1


def create_new_wall(canvas, laby_model):
    starting_point = select_starting_point(laby_model)
    debug("starting_point=", starting_point)

    if starting_point is not None:
        (row, column) = starting_point
        create_random_wall(laby_model, row, column, canvas)
        display(canvas, laby_model)

# 
# laby_model = [ [3, 0,   2,   2,   2,   2,   2,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [1, 0,   0,   0,   0,   0,   0,   1  ],
#                [2, 2,   2,   2,   2,   0,   2,   0  ]]

laby_model = []
N_COLUMNS = 15
N_ROWS = 15
laby_model.append([3, 0] + [2] * (N_COLUMNS-3) + [1])
for i in range(N_ROWS-2):
    laby_model.append([1] + [0] * (N_COLUMNS-2) + [1])
laby_model.append([2] * (N_COLUMNS-3) + [0, 2, 0])


CANVAS_HEIGHT = 500
CANVAS_WIDTH = 500
X_PACE = CANVAS_WIDTH / (len(laby_model[0]) + 1)
Y_PACE = CANVAS_HEIGHT / (len(laby_model) + 1)
X0 = X_PACE
Y0 = Y_PACE

#laby_model = randomize(laby_model[:])

#random.seed(0)

window = tkinter.Tk()

title = tkinter.Label(window, text="pylaby")
title.pack()
canvas = tkinter.Canvas(window, bg="white", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.pack()
window.bind('<KeyPress>', key_press)
timer = window.after(50, draw_next_wall, 1000)
window.stop_wall = False
window.mainloop()

