from pwn import context, remote, struct
import zlib
import random

context.log_level = 100

REM = remote('twisty-2mjh4xgp7zubo.shellweplayaga.me', 10000)
REM.recvuntil('Ticket please: ')
REM.sendline('ticket{WindwardPier4836n22:pd7pinOYiKO8ewdWu3NpQ3jXlYlCm03yuKzAkPkMXcQsZXbH}')
REM.recvuntil('Good luck')
REM.recvline()

ALL_DATA = []

def get_maze_floor():
    size = struct.unpack('i', REM.recv(4))[0]
    compressed_data = REM.recv(size)
    data = zlib.decompress(compressed_data).decode().replace('X','#')
    ALL_DATA.append(data)
    if "#" not in data:
        print(data)
    if "Congratulations!" in data:
        return "level solved","NSWEUD"
    if "Invalid Direction" in data:
        return "invalid", "NSWEUD"
    data = data.split('\n')
    maze_data, direcn_data = data[:-1], data[-1]
    allowed_directions = direcn_data[12:].split()[0]
    return [list(i) for i in maze_data], allowed_directions

def update_maze(maze, local_vision, floor):
    if floor not in maze:
        maze[floor] = local_vision
        return maze
    if len(local_vision)==0:
        return maze
    height = len(maze[floor])
    width = len(maze[floor][0])

    for i in range(height):
        for j in range(width):
            if maze[floor][i][j]=="@" and local_vision[i][j] not in '+-':
                maze[floor][i][j] = "."
            if local_vision[i][j]=='@':
                maze[floor][i][j]='@'
            if maze[floor][i][j]==" " and local_vision[i][j]!=" ":
                maze[floor][i][j] = local_vision[i][j]
    return maze

def print_maze(maze, current_level):
    result = "\n".join( "".join(i) for i in maze[current_level])
    if "E" in result:
        print("EXIT HERE",end="")
    print("floor:", current_level)
    print(result)


movemap = {i:j for i,j in zip("WASDQE","NWSEUD")}

while True:
    MAZE = {}
    maze_floor, allowed_directions = get_maze_floor()
    current_level = 0
    MAZE[current_level] = maze_floor
    print_maze(MAZE, current_level)
    while True:
        move = input("select {}\n".format(allowed_directions)).upper()
        move = movemap.get(move,"")
        while move=="" or move not in allowed_directions:
            move = input("try again {}\n".format(allowed_directions)).upper()
            move = movemap.get(move,"")
        if move == "U":
            current_level+=1
        elif move=="D":
            current_level-=1
        REM.sendline(move)
        new_local, allowed_directions = get_maze_floor()
        if new_local == "level solved":
            break
        elif new_local == "invalid":
            print_maze(MAZE, current_level)
            continue
        # if new_local is None: #we solved current level
        #     break
        MAZE = update_maze(MAZE, new_local, current_level)
        print_maze(MAZE, current_level)




