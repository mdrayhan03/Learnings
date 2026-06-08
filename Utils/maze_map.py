import random

# Easy: 11 x 11 (Quick to solve)
# Medium: 21 x 21 (Requires some thought)
# Hard: 41 x 41 (A screen-filling challenge)

def generate_maze(width, height):
    # Create a grid full of walls (#)
    maze = [["#"] * width for _ in range(height)]
    
    def walk(x, y):
        maze[y][x] = " " # Set current cell to path

        # Randomize directions: North, South, East, West
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(dirs)

        for dx, dy in dirs:
            # We move 2 steps at a time to jump over the 'wall'
            nx, ny = x + (dx * 2), y + (dy * 2)

            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == "#":
                maze[y + dy][x + dx] = " " # Remove wall between
                walk(nx, ny)

    walk(1, 1) # Start tunneling from (1,1)
    
    # Set Start and End
    maze[1][1] = "P"
    maze[height-2][width-2] = "E"
    return maze

# Example usage for "Medium" mode:
# current_maze = generate_maze(21, 21)

maze = generate_maze(41,41)

for m in maze :
    for ele in m :
        print(ele, end="")
    print()