import sys

def solution_to_string(maze, end):
    if end == (-1, -1):
        print("No solution")

    cell = end
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for i in range(maze[cell[0]][cell[1]]-1, 0, -1):
        neighbours = [(cell[0]+x, cell[1]+y) for x, y in dirs]
        for c in neighbours:
            if c[0] < 0 or c[0] > len(maze) - 1 or c[1] < 0 or c[1] > len(maze[0]) - 1:
                continue
            elif maze[c[0]][c[1]] == i:
                maze[c[0]][c[1]] = -3
                cell = c
                break
    
    maze[end[0]][end[1]] = -3
    
    s = ""

    for i in maze:
        for j in i:
            if j == -1:
                s += "#"
            elif j == -3:
                s += "*"
            else:
                s += " "
        s += "\n"

    return s
    

def bfs_maze_solver(maze, start):
    current_queue = [start]
    next_queue = []
    index = 1

    maze[start[0]][start[1]] = index

    while True:
        index += 1
        while len(current_queue) > 0:
            current = current_queue.pop()
            neighbours = get_unvisited_neighbours(maze, current)
            next_queue += neighbours
            for cell in neighbours:
                if maze[cell[0]][cell[1]] == -2:
                    maze[cell[0]][cell[1]] = index
                    return maze, cell
                maze[cell[0]][cell[1]] = index
        if len(next_queue) == 0:
            return maze, (-1, -1)
        current_queue = next_queue
        next_queue = []

def get_unvisited_neighbours(maze, cell):
    # Returns list of all neighbours of a given cell which have not yet visited
    # Param maze:
    # Param i and j: column and row of the cell
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbours = [(cell[0]+x, cell[1]+y) for x, y in dirs]
    unvisited_neighbours = []
    for c in neighbours:
        if c[0] < 0 or c[0] > len(maze) - 1 or c[1] < 0 or c[1] > len(maze[0]) - 1:
            continue
        if maze[c[0]][c[1]] == 0 or maze[c[0]][c[1]] == -2:
            unvisited_neighbours.append(c)

    return unvisited_neighbours

def parse_maze_file(file_path):
    f = open(file_path, "r")
    maze = []
    start = [0, 0]
    i = 0
    for l in f:
        line = []
        j = 0
        for c in l:
            if c == "#":
                line.append(-1)
            elif c == " ":
                line.append(0)
            elif c == "E":
                line.append(-2)
            elif c == "^":
                line.append(0)
                start = (i, j)
            j += 1
        maze.append(line)
        i += 1
    return maze, start

def main(argv):
    if len(argv) == 0:
        print("Missing input file")
        return
    maze, start = parse_maze_file(argv[0])
    solution, end_coords = bfs_maze_solver(maze, start)
    print(solution_to_string(solution, end_coords))

if __name__ == "__main__":
    main(sys.argv[1:])