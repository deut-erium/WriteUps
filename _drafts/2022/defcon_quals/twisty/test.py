def print_maze(maze):
    for row in maze:
        for item in row:
            print(item, end='')
        print()

def find_start(maze):
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            if maze[row][col] == '@':
                return row, col

def is_valid_position(maze, pos_r, pos_c):
    if pos_r < 0 or pos_c < 0:
        return False
    if pos_r >= len(maze) or pos_c >= len(maze[0]):
        return False
    if maze[pos_r][pos_c] in ' E':
        return True
    return False

def solve_maze(maze, start, stack):
    stack.append(start)

    pos_r, pos_c = start
    if maze[pos_r][pos_c] == 'E':
        # print(stack)
        return stack
    if maze[pos_r][pos_c] == 'X':
        stack.pop()
        return None
    # Mark position as visited
    maze[pos_r][pos_c] = 'X'
    # Check for all possible positions and add if possible
    if is_valid_position(maze, pos_r - 1, pos_c):
        if solve_maze(maze, (pos_r - 1, pos_c), stack) is not None:
            return stack
    if is_valid_position(maze, pos_r + 1, pos_c):
        if solve_maze(maze, (pos_r + 1, pos_c), stack) is not None:
            return stack
    if is_valid_position(maze, pos_r, pos_c - 1):
        if solve_maze(maze, (pos_r, pos_c - 1), stack) is not None:
            return stack
    if is_valid_position(maze, pos_r, pos_c + 1):
        if solve_maze(maze, (pos_r, pos_c + 1), stack) is not None:
            return stack
    stack.pop()
    return None

def update_maze(maze, start):
    # if there is a space where 3 of its surroundings are #, it means this is deadend
    while True:
        updated = False
        for i in range(1, len(maze)-1):
            for j in range(1, len(maze[i])-1):
                if maze[i][j] != ' ' or maze[i][j] == start:
                    continue
                cnt = (maze[i+1][j] == '#') + (maze[i-1][j] == '#') + (maze[i][j+1] == '#') + (maze[i][j-1] == '#')
                if cnt >= 3:
                    updated = True
                    maze[i][j] = '#'
        if not updated:
            return maze

def solve(data, prev_maze = None):
    maze = [[i for i in line] for line in data]
    # convert 'X' and 'S' to '#'
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'X':
                maze[i][j] = '#'
            if maze[i][j] == 'S':
                maze[i][j] = '#'
            if prev_maze is not None:
                if prev_maze[i][j] == '#' and maze[i][j] != '#':
                    maze[i][j] = '#'
    start = find_start(maze)
    # maze = update_maze(maze, start)
    maze_copy = [[i for i in line] for line in maze]
    print_maze(maze)
    stack = []
    full_path = solve_maze(maze, start, stack)
    directions = ''
    for i in range(len(full_path) - 1):
        x, y = full_path[i], full_path[i+1]
        if x[0]-y[0]==1:
            directions += 'N'
        elif y[0]-x[0]==1:
            directions += 'S'
        elif x[1]-y[1]==1:
            directions += 'W'
        else:
            assert y[1]-x[1]==1
            directions += 'E'
    return maze_copy, directions

from pwn import *
import zlib
import random

context.log_level = 100

# Start game
conn = remote('twisty-2mjh4xgp7zubo.shellweplayaga.me', 10000)
conn.recvuntil('Ticket please: ')
conn.sendline('ticket{WindwardPier4836n22:pd7pinOYiKO8ewdWu3NpQ3jXlYlCm03yuKzAkPkMXcQsZXbH}')
conn.recvuntil('Good luck')
conn.recvline()

opposite = {"N":"S", "S":"N", "W":"E", "E":"W"}

level1 = True
while True:
    data = conn.recv(4)
    size = struct.unpack('i', data)[0]
    data = conn.recv(size)
    res = zlib.decompress(data).decode()
    print(res)

    # Solve maze
    res = res.split('\n')
    res, next_dir = res[:-1], res[-1]
    maze_copy, directions = solve(res, None)
    previous_pick = 'S'
    for d in directions:
        if d not in next_dir:
            pos = next_dir[12:].split(" ")[0]
            conn.sendline(random.choice(pos))
        else:
            conn.sendline(d)
            previous_pick = d
        data = conn.recv(4)
        size = struct.unpack('i', data)[0]
        data = conn.recv(size)
        res = zlib.decompress(data).decode()
        print(res)
        if "Congratulations" in res:
            # We go to next level here
            level1 = False
            break
        res = res.split('\n')
        res, next_dir = res[:-1], res[-1]
        if d not in next_dir:
            maze_copy, directions = solve(res, maze_copy)
