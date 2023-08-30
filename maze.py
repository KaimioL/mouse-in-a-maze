import sys

def solution_to_string(maze, end):
    # Returns solved maze as string

    # Negative coordinates indicate that maze has no solution
    if end == (-1, -1):
        return "No solution"

    # Start from the last cell of the route
    cell = end
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # Iterate cells in reverse order starting from the last cell and going to neighbour with one less value
    for i in range(maze[cell[0]][cell[1]]-1, 0, -1):
        neighbours = [(cell[0]+x, cell[1]+y) for x, y in dirs]
        for c in neighbours:
            if c[0] < 0 or c[0] > len(maze) - 1 or c[1] < 0 or c[1] > len(maze[0]) - 1:
                # Neighbour out of bounds
                continue
            
            # If neighbour value is one less than current cells original value, chance its value to -3 to mark it as cell in optimal path
            elif maze[c[0]][c[1]] == i:
                maze[c[0]][c[1]] = -3
                cell = c
                break
    
    maze[end[0]][end[1]] = -3
    
    # Generate string out of the maze matrix
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
    # The algorithm uses breadth-first search to find the shortest route out of the maze

    current_queue = [start]
    next_queue = []
    index = 1

    # Set starting position value to one
    maze[start[0]][start[1]] = index

    while True:
        # Every steps cells are marked with one higher value
        index += 1

        # Iterate through all the cells in queue
        while len(current_queue) > 0:
            current = current_queue.pop()

            # Add all non-visited, non-wall neighboring cells to the next steps queue
            neighbours = get_unvisited_neighbours(maze, current)
            next_queue += neighbours
            for cell in neighbours:

                # If neighboring cell is end goal, return current maze as solved one
                # Otherwise mark neighbour with current index
                if maze[cell[0]][cell[1]] == -2:
                    maze[cell[0]][cell[1]] = index
                    return maze, cell
                maze[cell[0]][cell[1]] = index

        # If next steps queue is empty after iterating, maze has no solutions and negative value coordinates are returned
        if len(next_queue) == 0:
            return maze, (-1, -1)
        current_queue = next_queue
        next_queue = []

def get_unvisited_neighbours(maze, cell):
    # Returns list of all neighbours of a given cell which have not yet visited

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
    # Returns maze matrix and starting cell coords,
    # 0:  empty cell
    # -1: wall
    # -2: exit cell

    try:
        f = open(file_path, "r")
    except FileNotFoundError:
        print("Maze file doesn't exist")
        sys.exit(1)
    
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