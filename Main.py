import pygame
from Pet import Pet

pygame.init()
WIDTH, HEIGHT = 650, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pet Simulator")
font = pygame.font.Font(None, 28)

pet_image = pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/pet.png")
pet_image = pygame.transform.scale(pet_image, (140, 140))

background_image = pygame.image.load("/Users/krishiv/Documents/Python/Pet Simulator/assets/background.jpg")

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
        pygame.draw.rect(screen, self.hover_color if self.rect.collidepoint(mouse_pos) else self.color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
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
    screen.blit(pet_image, (350, 160))

def draw_stats():
    draw_bar("Hunger", pet.hunger, 20, 20, (255, 100, 100))      
    draw_bar("Happiness", pet.happiness, 20, 80, (100, 200, 255)) 
    draw_bar("Energy", pet.energy, 20, 140, (255, 255, 100))      
    draw_bar("Health", pet.health, 20, 200, (100, 255, 100))      

    level_text = font.render(f"Level: {pet.level}", True, (255, 180, 50))  
    screen.blit(level_text, (20, 260))

name = input("Enter pet name: ")
pet = Pet(name,)

clock = pygame.time.Clock()

buttons = [
    Button("Feed", 50, 330, 100, 40, pet.feed),
    Button("Play", 170, 330, 100, 40, pet.play),
    Button("Sleep", 290, 330, 100, 40, pet.sleep),
    Button("Wash", 410, 330, 100, 40, pet.wash),
    Button("Exit", 530, 330, 60, 40, quit)
]

running = True
while running:
    screen.blit(background_image, (0, 0))

    draw_stats()
    draw_pet()

    pygame.draw.rect(screen, (40, 40, 40), (0, 320, 650, 130))

    for button in buttons:
        button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_click(event)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
