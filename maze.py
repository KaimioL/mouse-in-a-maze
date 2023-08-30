import sys
import copy

def solution_to_string(maze, end):
    # Returns solved maze as string

    # Negative coordinates indicate that maze has no solution
    if end == (-1, -1):
        return "No solution"

    elif end == (-2, -2):
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
                if i == 1:
                    maze[c[0]][c[1]] = -4
                else:
                    maze[c[0]][c[1]] = -3
                cell = c
                break
    
    maze[end[0]][end[1]] = -5
    
    # Generate string out of the maze matrix
    s = ""

    for i in maze:
        for j in i:
            if j == -1:
                s += "#"
            elif j == -3:
                s += "."
            elif j == -4:
                s += "S"
            elif j == -5:
                s += "E"
            else:
                s += " "
        s += "\n"

    return s
    
def bfs_maze_solver(input_maze, start, max_steps):
    # The algorithm uses breadth-first search to find the shortest route out of the maze

    maze = copy.deepcopy(input_maze)
    current_queue = [start]
    next_queue = []
    index = 1

    # Set starting position value to one
    maze[start[0]][start[1]] = index

    while index < max_steps:
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

        # If next steps queue is empty after iterating, maze has no solutions and -1 value coordinates are returned
        if len(next_queue) == 0:
            return maze, (-1, -1)
        current_queue = next_queue
        next_queue = []
    
    # If no solution was found in maximum steps, -2 value coordinates are returned
    return maze, (-2, -2)

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
    solution, end_coords = bfs_maze_solver(maze, start, 20)

    if end_coords == (-1, -1):
        print("Maze can't be solved")
        return
    
    print("Max 20 steps: \n" + solution_to_string(solution, end_coords))
    solution, end_coords = bfs_maze_solver(maze, start, 150)
    print("Max 150 steps: \n" + solution_to_string(solution, end_coords))
    solution, end_coords = bfs_maze_solver(maze, start, 200)
    print("Max 200 steps: \n" + solution_to_string(solution, end_coords))

if __name__ == "__main__":
    main(sys.argv[1:])