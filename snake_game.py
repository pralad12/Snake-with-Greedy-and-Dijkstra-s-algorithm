import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

import pygame
import numpy as np
import heapq as h

import sys

from heapq import *

pygame.init()

# Defining the colors that the snake and food will use.  
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Width of the game board (in tiles). 
WIDTH = 20
# Height of the game board (in tiles).
HEIGHT = 20

# Size of each tile (in pixels).
STEPSIZE = 40

# How fast the game runs. Higher values are faster. 
CLOCK_SPEED = 10

# Making a pygame display. 
dis = pygame.display.set_mode((WIDTH * STEPSIZE, HEIGHT * STEPSIZE))
pygame.display.set_caption('Snake!')

# Initial variables to store the starting x and y position,
# and whether the game has ended. 
game_over = False
x1 = 5
y1 = 5
snake_list = [(x1, y1)]
snake_len = 1
x1_change = old_x1_change = 0
y1_change = old_y1_change = 0

# PyGame clock object.  
clock = pygame.time.Clock()

food_eaten = True

# Random obstacles, if desired. 
obstacles = [(np.random.randint(low=0, high=WIDTH), np.random.randint(low=0, high=HEIGHT)) for i in
             range(int(sys.argv[2]))]


# This method is a wrapper for the various AI methods.
# right now it just moves the snake randomly regardless
# of the board state, because none of those methods are 
# filled in yet. 
# Bstate is a matrix representing the game board:
### Array cells with a 0 are empty locations. 
### Array cells with a -1 are the body of the snake.
### The cell marked with a -2 is the head of the snake.
### The cell marked with a 1 is the food.
def get_AI_moves(ai_mode, bstate):
    if ai_mode == 'rand':
        return random_AI(bstate)
    elif ai_mode == 'greedy':
        return greedy_AI(bstate)
    elif ai_mode == 'dijkstra':
        return dijkstra_AI(bstate)
    else:
        raise NotImplementedError("Not a valid AI mode!\nValid modes are rand, greedy, astar, dijkstra, and backt.")

    # These are the methods you will fill in.


# Only worry about the method assigned on a given day.
# Each method takes in a game board (as described above), and
# should output a series of moves. Valid moves are: 
# (0,1),(0,-1),(1,0), and (-1,0). This means if you want to
# move in any more complicated way, you need to convert the move
# you want to make into a sequence like this one.
# For example, if I wanted my snake to move +5 in the x direction and +3
# in the y direction, I could return 
# [(0,1),(0,1),(0,1),(0,1),(0,1),(1,0),(1,0),(1,0)].

# Several of these methods demonstrate how to get the source
# and target locations, but currently do not use this information.
def dijkstra_AI(bstate):

    source = np.array(np.where(bstate == -2))
    source = (int(source[0]), int(source[1]))
    target = np.array(np.where(bstate == 1))
    target = (int(target[0]), int(target[1]))
    queue = []
    priorities = {}
    visited = []
    path = {source: None}


    for i in range(len(bstate)):
        for j in range(len(bstate[i])):
            if bstate[i][j] == -2:
                h.heappush(queue, (0, (i,j)))
                priorities[(i, j)] = 0
            else:
                h.heappush(queue, (float('inf'), (i, j)))
                priorities[(i,j)] = (float('inf'))

    while len(queue) > 0:
        #Get position with lowest priority
        new_spot = h.heappop(queue)[1]
        #Check if not visited
        if new_spot not in visited:
            if new_spot == target:
                break
            #Mark as visited
            visited.append(new_spot)
            neighbors = []
            x_cord = new_spot[0]
            y_cord = new_spot[1]
            if x_cord + 1 < WIDTH:
                right = ((x_cord + 1, y_cord))
                neighbors.append(right)
            else:
                right = ((0, y_cord))
                neighbors.append(right)
            if x_cord - 1 >= 0:
                left = ((x_cord - 1, y_cord))
                neighbors.append(left)
            else:
                left = ((WIDTH - 1, y_cord))
                neighbors.append(left)
            if y_cord + 1 < HEIGHT:
                up = ((x_cord, y_cord + 1))
                neighbors.append(up)
            else:
                up = ((x_cord, 0))
                neighbors.append(up)
            if y_cord - 1 >= 0:
                down = ((x_cord, y_cord - 1))
                neighbors.append(down)
            else:
                down = ((x_cord, HEIGHT - 1))
                neighbors.append(down)
            #For each unvisited  neighbor, update its priority in queue
            for neighbor in neighbors:
                found = False
                if neighbor not in visited and bstate[neighbor] != -1:
                    if priorities[new_spot] + 1 < priorities[neighbor]:
                        for i,item in enumerate(queue):
                            if item[1] == neighbor:
                                found = True
                                queue[i] = (priorities[new_spot] + 1, item[1])
                                h.heapify(queue)
                        if not found:
                            h.heappush(queue, (priorities[new_spot] + 1, item[1]))

                        priorities[neighbor] = priorities[new_spot] + 1
                        path[neighbor] = new_spot

    if target not in path.keys():
        return [(-1,0)]

    to_return = []
    goal = target
    while goal is not None:
        x_pos, y_pos = goal
        goal = path[goal]
        if goal is not None:
            neighbor_x, neighbor_y = goal
            x_move = x_pos - neighbor_x
            y_move = y_pos - neighbor_y
            to_return.append((x_move, y_move))


    return to_return[::-1]



def greedy_AI(bstate):
    source = np.array(np.where(bstate == -2))
    target = np.array(np.where(bstate == 1))

    if source[0] > target[0]:
        return [(-1,0)]
    elif source[0] < target[0]:
        return [(1,0)]
    elif source[1] > target[1]:
        return [(0,-1)]
    elif source[1] < target[1]:
        return [(0,1)]


def random_AI(bstate):
    return [[(0, 1), (0, -1), (1, 0), (-1, 0)][np.random.randint(low=0, high=4)]]


mode = sys.argv[1]

AI_moves = []

# Don't modify any code below this point!
# This code is not meant to be readable or understandable to you - it's the game
# engine and the particulars of moving the snake according to your AI.
# The particulars of the code below shouldn't matter to your AI code above.
# If you have questions, or if your AI code needs to be able to use any of the below,
# talk to or email Cory.  

while not game_over:

    if food_eaten:
        fx = np.random.randint(low=0, high=WIDTH)
        fy = np.random.randint(low=0, high=HEIGHT)
        while (fx, fy) in snake_list or (fx, fy) in obstacles:
            fx = np.random.randint(low=0, high=WIDTH)
            fy = np.random.randint(low=0, high=HEIGHT)
        food_eaten = False

    dis.fill(white)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if mode == 'human':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -1
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = 1
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -1
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = 1
                    x1_change = 0
    if mode != 'human':
        if len(AI_moves) == 0:
            bstate = np.zeros((WIDTH, HEIGHT))
            for xx, yy in snake_list:
                bstate[xx, yy] = -1
            for xx, yy in obstacles:
                bstate[xx, yy] = -1
            bstate[snake_list[-1][0], snake_list[-1][1]] = -2
            bstate[fx, fy] = 1
            AI_moves = get_AI_moves(mode, bstate)
        x1_change, y1_change = AI_moves.pop(0)
    if len(snake_list) > 1:
        if ((snake_list[-1][0] + x1_change) % WIDTH) == snake_list[-2][0] and (
                (snake_list[-1][1] + y1_change) % HEIGHT) == snake_list[-2][1]:
            x1_change = old_x1_change
            y1_change = old_y1_change
    x1 += x1_change
    y1 += y1_change

    x1 = x1 % WIDTH
    y1 = y1 % HEIGHT

    if x1 == fx and y1 == fy:
        snake_len += 1
        food_eaten = True

    snake_list.append((x1, y1))
    snake_list = snake_list[-snake_len:]

    if len(list(set(snake_list))) < len(snake_list) or len(set(snake_list).intersection(set(obstacles))) > 0:
        print("You lose! Score: %d" % snake_len)
        game_over = True
    else:
        sncols = np.linspace(.5, 1.0, len(snake_list))
        for jj, (xx, yy) in enumerate(snake_list):
            pygame.draw.rect(dis, (0, 255 * sncols[jj], 32 * sncols[jj]),
                             [xx * STEPSIZE, yy * STEPSIZE, STEPSIZE, STEPSIZE])

        for (xx, yy) in np.cumsum(np.array([[.5, .5], snake_list[-1]] + AI_moves), axis=0)[2:]:
            pygame.draw.circle(dis, red, (xx * STEPSIZE, yy * STEPSIZE), STEPSIZE / 4)

        if not food_eaten:
            pygame.draw.rect(dis, red, [fx * STEPSIZE, fy * STEPSIZE, STEPSIZE, STEPSIZE])

        for xx, yy in obstacles:
            pygame.draw.rect(dis, blue, [xx * STEPSIZE, yy * STEPSIZE, STEPSIZE, STEPSIZE])
        pygame.display.update()

        clock.tick(CLOCK_SPEED)

        old_x1_change = x1_change
        old_y1_change = y1_change

pygame.quit()
quit()
