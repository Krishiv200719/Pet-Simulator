import pickle

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

    def feed(self):
        print(f"{self.name} is eating...")
        self.hunger -= 20
        self.health += 5
        self.happiness += 5
        self.gain_xp(10)
        self.update_stats()

    def play(self):
        print(f"{self.name} loves playing!")
        self.happiness += 20
        self.energy -= 20
        self.hunger += 10
        self.gain_xp(15)
        self.update_stats()

    def sleep(self):
        print(f"{self.name} is sleeping...zzz")
        self.energy += 25
        self.health += 10
        self.hunger += 5
        self.gain_xp(5)
        self.update_stats()

    def wash(self):
        print(f"You are cleaning {self.name}...")
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
            print(f"Congratulations! {self.name} reached Level {self.level}!")

    def update_stats(self):
        if self.energy <= 20:
            self.happiness -= 10
            print(f"{self.name} feels tired and unhappy.")

        if self.hunger >= 80:
            self.happiness -= 10
            print(f"{self.name} is feeling very hungry.")

        if self.hunger >= 100:
            print(f"\nALERT: {self.name} is starving and suffering!")
            self.health -= 10

        if self.hunger <= 0:
            print(f"\nALERT: {self.name} is overfed and feeling sick!")
            self.health -= 10

        stats = ['hunger', 'happiness', 'energy', 'health']
        for attr in stats:
            value = getattr(self, attr)
            setattr(self, attr, max(0, min(100, value)))

        if self.energy == 0:
            print(f"\n{self.name} collapsed from exhaustion!")

        if self.health == 0:
            print(f"\nCRITICAL ALERT: {self.name} has died...")
            self.is_dead = True

    def show_status(self):
        print("\n===== Pet Status =====")
        print(f"Name: {self.name}")
        print(f"Hunger: {self.hunger}")
        print(f"Happiness: {self.happiness}")
        print(f"Energy: {self.energy}")
        print(f"Health: {self.health}")
        print(f"Level: {self.level}")
        print("=======================\n")

    def save(self):
        with open("/Users/krishiv/Documents/Python/Pet Simulator/savegame.dat", "wb") as file:
            pickle.dump(self, file)
        print("Game Saved.")