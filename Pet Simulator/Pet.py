import random

class Pet:
    def __init__(self, name):
        self.name = name
        
        self.hunger = 50
        self.happiness = 50
        self.energy = 50
        self.health = 50
        
        self.level = 1
        self.experience = 0
        
        self.is_dead = False

        self.state = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.action_timer = 0

        self.blink_timer = 0
        self.blink_delay = random.randint(60, 200)

    def update_animation(self, animation_length, idle_animation_length):
        if self.is_dead:
            return
        
        self.animation_timer += 1
        
        if self.state == "idle":
            if self.animation_timer >= 12:
                self.animation_timer = 0
                self.animation_frame = (self.animation_frame + 1) % idle_animation_length
            
            self.blink_timer += 1
            if self.blink_timer > self.blink_delay:
                self.animation_frame = 1
                if self.blink_timer > self.blink_delay + 10:
                    self.blink_timer = 0
                    self.blink_delay = random.randint(60, 200)
        
        else:
            if self.animation_timer >= 7:
                self.animation_timer = 0
                self.animation_frame += 1
                if self.animation_frame >= animation_length:
                    self.animation_frame = 0
            
            self.action_timer -= 1
            if self.action_timer <= 0:
                self.state = "idle"

    def start_action(self, state, duration):
        if not self.is_dead:
            self.state = state
            self.animation_frame = 0
            self.animation_timer = 0
            self.action_timer = duration

    def feed(self):
        self.start_action("eat", 25)
        self.hunger -= 20
        self.health += 5
        self.energy += 10
        self.happiness += 5
        self.gain_xp(10)
        self.update_stats()

    def play(self):
        self.start_action("play", 40)
        self.happiness += 20
        self.energy -= 20
        self.hunger += 10
        self.gain_xp(15)
        self.update_stats()

    def sleep(self):
        self.start_action("sleep", 50)
        self.energy += 25
        self.health += 10
        self.hunger += 5
        self.gain_xp(5)
        self.update_stats()

    def wash(self):
        self.start_action("wash", 30)
        self.health += 15
        self.happiness -= 5
        self.energy -= 5
        self.hunger += 7
        self.gain_xp(8)
        self.update_stats()

    def gain_xp(self, amount):
        self.experience += amount
        if self.experience >= 50:
            self.level += 1
            self.experience = 0

    def update_stats(self):
        if self.energy <= 20:
            self.happiness -= 10

        if self.hunger >= 80:
            self.happiness -= 10

        if self.hunger >= 100:
            self.health -= 10

        if self.hunger <= 0:
            self.health -= 10

        for attr in ['hunger', 'happiness', 'energy', 'health']:
            setattr(self, attr, max(0, min(100, getattr(self, attr))))

        if self.health == 0:
            self.is_dead = True