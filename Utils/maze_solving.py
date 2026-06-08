import os
from maze_map import generate_maze

# 1. Define the Maze (0 = path, 1 = wall)
maze = generate_maze(11, 11)

# Player starting position
player_pos = [1, 1] 

def draw_maze():
    os.system('cls' if os.name == 'nt' else 'clear') # Clears the terminal
    for row in maze:
        print(" ".join(row))

while True:
    draw_maze()
    move = input("Move (WASD): ").lower()
    
    # Calculate potential new position
    row, col = player_pos
    new_row, new_col = row, col

    if move == "w": new_row -= 1
    elif move == "s": new_row += 1
    elif move == "a": new_col -= 1
    elif move == "d": new_col += 1
    elif move == "q": break

    # 2. Collision Logic
    if maze[new_row][new_col] == "E":
        print("You found the exit! 🏆")
        break
    elif maze[new_row][new_col] == " ":
        # Update the grid
        maze[row][col] = " "        # Leave old spot
        maze[new_row][new_col] = "P" # Move to new spot
        player_pos = [new_row, new_col]