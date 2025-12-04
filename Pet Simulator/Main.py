import pygame
import pickle
import os
from Pet import Pet
import random
import math

pygame.init()
WIDTH, HEIGHT = 650, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet Simulator")
font = pygame.font.Font(None, 28)

save_path = "/Users/krishiv/Documents/Python/Pet Simulator/savegame.dat"

clouds_moving = True

pet_image = pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/pet.png")
pet_image = pygame.transform.scale(pet_image, (140, 140))

ghost_image = pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/Ghost.png")
ghost_image = pygame.transform.scale(ghost_image, (140, 140))

background_image = pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/background.png")
background_image = pygame.transform.scale(background_image, (650, 350))

cloud_images = [
    pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/cloud1.webp"),
    pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/cloud2.webp"),
    pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/cloud3.png")
]
cloud_images = [pygame.transform.scale(img, (100, 60)) for img in cloud_images]

cloud_start_positions = [
    (100, 30),
    (300, 50),
    (500, 20)
]

import math

class Cloud:
    def __init__(self, image, start_x, start_y, depth):
        self.image = image.convert_alpha()
        self.x = start_x
        self.base_y = start_y
        self.y = start_y

        self.depth = depth  
        self.speed = 1.5 / depth
        transparency_value = max(60, 255 - depth * 60)
        self.image.set_alpha(transparency_value)

        self.drift_angle = random.uniform(0, math.pi * 2)
        self.drift_speed = random.uniform(0.01, 0.03) * (1 / depth)
        self.drift_range = random.uniform(5, 12)

    def move(self):
        self.x -= self.speed
        if self.x < -150:
            self.x = 700  

        self.drift_angle += self.drift_speed
        self.y = self.base_y + math.sin(self.drift_angle) * self.drift_range

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

def text_input(prompt):
    input_text = ""
    typing = True
    while typing:
        screen.blit(background_image, (0, 0))
        prompt_surface = font.render(prompt, True, (255, 255, 255))
        screen.blit(prompt_surface, (20, 100))
        input_surface = font.render(input_text + "|", True, (255, 255, 255))
        screen.blit(input_surface, (20, 150))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_popup()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
    return input_text

def save_pet(pet):
    with open(save_path, "wb") as f:
        pickle.dump(pet, f)
    print("Game Saved")

def load_pet():
    try:
        with open(save_path, "rb") as f:
            print("Loaded saved pet.")
            return pickle.load(f)
    except:
        print("No save found. Starting new pet.")
        return None

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (0, 170, 255)
        self.hover_color = (80, 220, 255)
        self.callback = callback
        self.font = pygame.font.Font(None, 30)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.rect(
            screen,
            self.hover_color if self.rect.collidepoint(mouse_pos) else self.color,
            self.rect,
            border_radius=12
        )
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        screen.blit(text_surface, text_surface.get_rect(center=self.rect.center))

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

def draw_bar(label, value, x, y, color):
    txt = font.render(f"{label}: {value}", True, color)
    screen.blit(txt, (x, y))
    pygame.draw.rect(screen, (60, 60, 60), (x, y + 22, 200, 20))
    bar_width = int((value / 100) * 200)
    pygame.draw.rect(screen, color, (x, y + 22, bar_width, 20))

def draw_pet():
    image = ghost_image if pet.is_dead else pet_image
    screen.blit(image, (350, 160))

def draw_stats():
    draw_bar("Hunger", pet.hunger, 20, 20, (255, 100, 100))
    draw_bar("Happiness", pet.happiness, 20, 80, (100, 200, 255))
    draw_bar("Energy", pet.energy, 20, 140, (255, 255, 100))
    draw_bar("Health", pet.health, 20, 200, (100, 255, 100))
    level_text = font.render(f"Level: {pet.level}", True, (255, 180, 50))
    screen.blit(level_text, (20, 260))

def restart():
    global pet, clouds_moving
    clouds_moving = True
    if os.path.exists(save_path):
        os.remove(save_path)
    name = text_input("Enter pet name:")
    pet = Pet(name)

def game_over_screen():
    global clouds_moving
    clouds_moving = False

    if os.path.exists(save_path):
        os.remove(save_path)

    btn_restart = Button("Restart", 220, 300, 100, 40, restart)
    btn_quit = Button("Quit", 360, 300, 80, 40, lambda: (pygame.quit(), exit()))
    popup_buttons = [btn_restart, btn_quit]

    while pet.is_dead:
        screen.blit(background_image, (0, 0))
        for cloud in clouds:
            cloud.draw()

        draw_pet()
        msg = font.render(f"{pet.name} has died...", True, (255, 50, 50))
        msg2 = font.render("Game Over!", True, (255, 255, 255))
        screen.blit(msg, (225, 180))
        screen.blit(msg2, (260, 210))

        for b in popup_buttons:
            b.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            for b in popup_buttons:
                b.check_click(event)

def quit_popup():
    global clouds_moving
    clouds_moving = False
    popup_running = True

    def save_and_quit():
        save_pet(pet)
        pygame.quit()
        exit()

    def quit_without_saving():
        pygame.quit()
        exit()

    def cancel():
        nonlocal popup_running
        popup_running = False
        globals()["clouds_moving"] = True

    btn_save = Button("Save & Quit", 120, 280, 140, 40, save_and_quit)
    btn_quit = Button("Quit", 300, 280, 100, 40, quit_without_saving)
    btn_cancel = Button("Cancel", 430, 280, 120, 40, cancel)
    popup_buttons = [btn_save, btn_quit, btn_cancel]

    while popup_running:
        screen.blit(background_image, (0, 0))
        for cloud in clouds:
            cloud.draw()
        draw_stats()
        draw_pet()

        pygame.draw.rect(screen, (50, 50, 50), (80, 200, 500, 150), border_radius=15)
        msg = font.render("Save before quitting?", True, (255, 255, 255))
        screen.blit(msg, (210, 220))

        for b in popup_buttons:
            b.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit_without_saving()
            for b in popup_buttons:
                b.check_click(event)

pet = load_pet()
if pet is None:
    name = text_input("Enter pet name:")
    pet = Pet(name)

clouds = [
    Cloud(cloud_images[0], cloud_start_positions[0][0], cloud_start_positions[0][1], depth=1),
    Cloud(cloud_images[1], cloud_start_positions[1][0], cloud_start_positions[1][1], depth=2),
    Cloud(cloud_images[2], cloud_start_positions[2][0], cloud_start_positions[2][1], depth=3)
]

buttons = [
    Button("Feed", 80, 350, 100, 40, pet.feed),
    Button("Play", 190, 350, 100, 40, pet.play),
    Button("Sleep", 360, 350, 100, 40, pet.sleep),
    Button("Wash", 470, 350, 100, 40, pet.wash),
    Button("Save", 10, 400, 60, 40, lambda: save_pet(pet)),
    Button("Exit", 580, 400, 60, 40, quit_popup)
]

clock = pygame.time.Clock()
running = True

while running:
    screen.blit(background_image, (0, 0))

    for cloud in clouds:
        if clouds_moving:
            cloud.move()
        cloud.draw()

    draw_stats()
    draw_pet()

    if pet.is_dead:
        pygame.display.update()
        pygame.time.delay(500)
        game_over_screen()

    for button in buttons:
        button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_popup()
        if not pet.is_dead:
            for button in buttons:
                button.check_click(event)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
