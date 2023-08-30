def print_solution():
    print("aaa")

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
                    return maze, cell
                maze[cell[0]][cell[1]] = index
            
        current_queue = next_queue
        next_queue = []

def get_unvisited_neighbours(maze, cell):

    # Returns list of all neighbours of a given cell which have not yet visited
    # Param maze:
    # Param i and j: column and row of the cell
    print(maze)
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
    maze = []


def main():
    maze = [[0, 0, 0, -2],[0, -1, -1, 0]]
    maze, end = bfs_maze_solver(maze, [0, 0])
    for i in maze:
        print(i)

if __name__ == "__main__":
    main()