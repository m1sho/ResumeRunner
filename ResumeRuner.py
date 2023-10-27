import pygame
import random
import PyPDF2
import tkinter as tk
from tkinter import filedialog


pygame.init()

# player constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
FONT_SIZE = 36
PLAYER_SPEED = 5
ENEMY_SPEED = 1
ENEMY_HEALTH = 1
PLAYER_HEALTH = 100
COLORS = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
}

#window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Word Shooter")


font = pygame.font.Font(None, FONT_SIZE)

user_name = ""

# file (either text or PDF)
def read_words_from_file(file_path):
    words = []
    try:
        if file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                words = file.read().split()
        elif file_path.endswith(".pdf"):
            with open(file_path, 'rb') as file:
                pdf = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf.pages)):
                    page = pdf.pages[page_num]
                    words += page.extract_text().split()
        else:
            print("Unsupported file type.")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    return words


file_path = ''


words = []

# Player attributes
player_x = 50
player_y = HEIGHT // 2
player_shape = pygame.Rect(player_x, player_y, 20, 20)
player_health = PLAYER_HEALTH
player_score = 0
player_color = COLORS["red"]

# Enemies
enemies = []

# Function to shoot a letter at the enemies
def shoot_letter(letter):
    global player_score
    for enemy in enemies:
        if enemy[2].startswith(letter):
            enemy[2] = enemy[2][1:]  # Remove the first letter
            if not enemy[2]:
                player_score += 1
                enemies.remove(enemy)
            break

# Game loop
running = False
clock = pygame.time.Clock()

# Attack loop
typing_buffer = []

# Character customization settings
customization = {
    "shape": "square",
    "color": "red"
}

# Initialize Tkinter
root = tk.Tk()
root.title("Character Customization")

def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Text and PDF Files", "*.txt *.pdf")])

def start_game():
    global running, words, user_name, player_x, player_y, player_shape, player_health, player_score, enemies, typing_buffer
    running = True
    user_name = input_name.get()
    words = read_words_from_file(file_path)
    player_x = WIDTH // 4
    player_y = HEIGHT // 2
    player_shape = pygame.Rect(player_x, player_y, 20, 20)
    player_health = PLAYER_HEALTH
    player_score = 0
    enemies = []
    typing_buffer = []
    root.destroy()

def change_shape(new_shape):
    customization["shape"] = new_shape
    root.destroy()

def change_color(new_color):
    customization["color"] = new_color
    root.destroy()

# Create a menu
menu = tk.Menu(root)
root.config(menu=menu)

# File menu
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Choose File", command=choose_file)
file_menu.add_separator()
file_menu.add_command(label="Quit", command=root.quit)

# Character customization menu
character_menu = tk.Menu(menu)
menu.add_cascade(label="Character Customization", menu=character_menu)
character_menu.add_command(label="Change Shape", command=lambda: change_shape("square"))
character_menu.add_command(label="Change Color to Red", command=lambda: change_color("red"))
character_menu.add_command(label="Change Color to Green", command=lambda: change_color("green"))
character_menu.add_command(label="Change Color to Blue", command=lambda: change_color("blue"))
character_menu.add_command(label="Change Color to Yellow", command=lambda: change_color("yellow"))

input_name_label = tk.Label(root, text="Enter Your Name:")
input_name_label.pack()
input_name = tk.Entry(root)
input_name.pack()

start_button = tk.Button(root, text="Start Game", command=start_game)
start_button.pack()

root.mainloop()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # Detect the Esc key for quitting
    if keys[pygame.K_ESCAPE]:
        print("Quitting...")
        running = False

    # Player movement
    if keys[pygame.K_UP]:
        player_shape.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_shape.y += PLAYER_SPEED

    # Spawn enemies
    if random.random() < 0.1:
        enemy_y = random.randint(0, HEIGHT - FONT_SIZE)
        if words:
            enemy_text = random.choice(words)
            enemies.append([WIDTH, enemy_y, enemy_text, ENEMY_HEALTH])

    # Update enemy positions
    for enemy in enemies:
        enemy[0] -= ENEMY_SPEED

    # Collision detection
    for enemy in enemies:
        if player_shape.colliderect(enemy[0], enemy[1], len(enemy[2]) * FONT_SIZE, FONT_SIZE):
            player_health -= 10
            enemies.remove(enemy)
        elif enemy[0] < 0:
            player_score += 1
            enemies.remove(enemy)

    # Shoot the user's name
    for letter in user_name:
        shoot_letter(letter)

    # Clear the typing buffer
    typing_buffer = []

    # Draw everything
    screen.fill(WHITE)
    pygame.draw.rect(screen, player_color, player_shape)

    for enemy in enemies:
        text = font.render(enemy[2], True, (0, 0, 0))
        screen.blit(text, (enemy[0], enemy[1))

    # Render user name scrolling words in black
    for user_name_word in user_name_words:
        user_name_text = font.render(user_name_word, True, (0, 0, 0))
        screen.blit(user_name_text, (user_name_x, user_name_y))

    # Display score and health
    score_text = font.render(f"Score: {player_score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 150, 10))
    health_text = font.render(f"Health: {player_health}", True, (0, 0, 0))
    screen.blit(health_text, (10, 10))

    # Game over condition
    if player_health <= 0:
        running = False

    pygame.display.flip()
    clock.tick(60)

# Game over screen
game_over_text = font.render("Game Over", True, (255, 0, 0))
screen.blit(game_over_text, (WIDTH // 2 - FONT_SIZE, HEIGHT // 2 - FONT_SIZE))
pygame.display.flip()

#  key press to exit loop
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
            waiting = False

pygame.quit()
