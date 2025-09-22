import random
from termcolor import colored


# ==============================
# GAME CONFIGURATION
# ==============================

# --- Game board ---
game_map = [
    "|--------|",
    "|G..|..G.|",
    "|...PP...|",
    "|G....@|.|",
    "|...P..|.|",
    "|--------|"
]

# --- UI representations ---
ui_wall = [
    "......",
    "......",
    "......",
    "......"
]

ui_ghost = [
    " .-.  ",
    "| OO| ",
    "|   | ",
    "'^^^' "
]

ui_hero = [
    " .--. ",
    "/ _.-'",
    "\\  '-.",
    " '--' "
]

ui_empty = [
    "      ",
    "      ",
    "      ",
    "      "
]

ui_pill = [
    "      ",
    " .-.  ",
    " '-'  ",
    "      "
]

# --- Colors ---
wall_color = "blue"
ghost_color = "red"
pacman_color = "yellow"
pill_color = "grey"


# ==============================
# GAME STATE
# ==============================

game_finished = False
win = False


# ==============================
# MAIN GAME LOOP
# ==============================
while not game_finished:

    # --------------------------
    # Draw the board
    # --------------------------
    for row in game_map:
        for piece in range(4):
            for point in row:
                if point == 'G':
                    print(colored(ui_ghost[piece], ghost_color), end='')
                elif point in '|-':
                    print(colored(ui_wall[piece], wall_color), end='')
                elif point == '@':
                    print(colored(ui_hero[piece], pacman_color), end='')
                elif point == '.':
                    print(ui_empty[piece], end='')
                elif point == 'P':
                    print(colored(ui_pill[piece], pill_color), end='')
            print()
    print()  # Extra space between frames


    # --------------------------
    # Move ghosts
    # --------------------------
    all_ghosts = []
    for x in range(len(game_map)):
        for y in range(len(game_map[x])):
            if game_map[x][y] == 'G':
                all_ghosts.append([x, y])

    for ghost in all_ghosts:
        old_x, old_y = ghost
        possible_directions = [
            [old_x, old_y + 1],  # right
            [old_x + 1, old_y],  # down
            [old_x, old_y - 1],  # left
            [old_x - 1, old_y]   # up
        ]

        random.shuffle(possible_directions)  # pick a random valid direction
        for next_x, next_y in possible_directions:
            if 0 <= next_x < len(game_map) and 0 <= next_y < len(game_map[0]):
                if game_map[next_x][next_y] not in '|-G':
                    if game_map[next_x][next_y] == '@':
                        game_finished = True
                        win = False
                    else:
                        game_map[old_x] = game_map[old_x][:old_y] + "." + game_map[old_x][old_y+1:]
                        game_map[next_x] = game_map[next_x][:next_y] + "G" + game_map[next_x][next_y+1:]
                    break

    if game_finished:
        break


    # --------------------------
    # Find Pac-Man
    # --------------------------
    pacman_x = pacman_y = -1
    for x in range(len(game_map)):
        for y in range(len(game_map[x])):
            if game_map[x][y] == '@':
                pacman_x, pacman_y = x, y


    # --------------------------
    # Eat pill
    # --------------------------
    if game_map[pacman_x][pacman_y] == 'P':
        game_map[pacman_x] = game_map[pacman_x][:pacman_y] + '@' + game_map[pacman_x][pacman_y+1:]


    # --------------------------
    # Check win condition
    # --------------------------
    pills_left = any('P' in row for row in game_map)
    if not pills_left:
        win = True
        game_finished = True
        break


    # --------------------------
    # Pac-Man movement
    # --------------------------
    while True:
        key = input("Move (w/a/s/d): ")
        if key not in ['w', 'a', 's', 'd']:
            print("Invalid key! Try again.")
            continue

        next_x, next_y = pacman_x, pacman_y
        if key == 'w': next_x -= 1
        if key == 's': next_x += 1
        if key == 'a': next_y -= 1
        if key == 'd': next_y += 1

        # Check bounds
        if not (0 <= next_x < len(game_map) and 0 <= next_y < len(game_map[0])):
            print("Out of bounds! Try again.")
            continue
        # Check wall
        if game_map[next_x][next_y] in '|-':
            print("Hit a wall! Try again.")
            continue
        # Check ghost
        if game_map[next_x][next_y] == 'G':
            game_finished = True
            win = False
            break

        # Valid move, update map
        game_map[pacman_x] = game_map[pacman_x][:pacman_y] + '.' + game_map[pacman_x][pacman_y+1:]
        game_map[next_x] = game_map[next_x][:next_y] + '@' + game_map[next_x][next_y+1:]
        break  # exit input loop


# ==============================
# GAME END
# ==============================
final_color = "red" if win else "green"

for row in game_map:
    for piece in range(4):
        for point in row:
            if point == 'G':
                print(colored(ui_ghost[piece], final_color), end='')
            elif point in '|-':
                print(colored(ui_wall[piece], final_color), end='')
            elif point == '@':
                print(colored(ui_hero[piece], final_color), end='')
            elif point == '.':
                print(colored(ui_empty[piece], final_color), end='')
            elif point == 'P':
                print(colored(ui_pill[piece], final_color), end='')
        print()
print()

# Final message
if win:
    print("You win! :)")
else:
    print("You lost! :/")