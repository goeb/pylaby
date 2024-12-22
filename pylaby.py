import random
import sys
import tkinter

def key_press(event):
    t = event.keysym
    if t == 'q':
        print('quit...')
        sys.exit(0)

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
    # If not found after 1000 attempts, then consider that no starting point is available
    while count < 1000:
        count += 1
        random_row = int(random.uniform(0, len(laby_model)))
        random_column = int(random.uniform(0, len(laby_model[0])))
        is_good = is_good_starting_point(laby_model, random_row, random_column)
        print(is_good)
        if is_good:
            return (random_row, random_column)

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

def create_random_wall(laby_model, row, column):
    # Get possible directions "up", "left", "right", "down"
    # right?

    n_walls = 4
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
    
        print("possibilities=", possibilities)

        if len(possibilities) == 0:
            return False

        # Choose a possibiity of direction
        direction = possibilities[int(random.uniform(0, len(possibilities)))]
        print("chosen=", direction)

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


CANVAS_HEIGHT = 1000
CANVAS_WIDTH = 1000
X_PACE = CANVAS_WIDTH / (len(laby_model[0]) + 1)
Y_PACE = CANVAS_HEIGHT / (len(laby_model) + 1)
X0 = X_PACE
Y0 = Y_PACE

#laby_model = randomize(laby_model[:])

random.seed(0)

window = tkinter.Tk()

title = tkinter.Label(window, text="pylaby")
title.pack()
canvas = tkinter.Canvas(window, bg="white", height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
#line = canvas.create_line(10, 10, 200, 200, fill='black')

count = 0
while count < 1000:
    count += 1
    starting_point = select_starting_point(laby_model)
    if starting_point is None:
        break
    (row, column) = starting_point
    print("starting_point=", starting_point)
    #canvas.create_text(X0+X_PACE*column, Y0+Y_PACE*row, text='x')
    create_random_wall(laby_model, row, column)

display(canvas, laby_model)

canvas.pack()
window.bind('<KeyPress>', key_press)
window.mainloop()

