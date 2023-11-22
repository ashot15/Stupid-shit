class character:
    def __init__(self, damage, speed, health):
        self.damage = damage
        self.speed = speed
        self.health = health


class monster:
    def __init__(self, damage, speed, health):
        self.damage = damage
        self.speed = speed
        self.health = health
warrior = character(5,20,100)
monster = character(6,25,150)
print(f"Warrior attributes: \n health {warrior.health}\n Damage {warrior.damage}\n Speed {warrior.speed}")
print(f"Monster attributes: \n health {monster.health}\n Damage {monster.damage}\n Speed {monster.speed}")


