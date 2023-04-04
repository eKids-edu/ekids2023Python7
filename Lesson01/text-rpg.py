import random

# Головний код гри
print("Ласкаво просимо до гри!")
player_name = input("Введіть своє ім'я: ")

player_health = 100
player_strength = 10

enemy_name = "Монстр"
enemy_health = 50
enemy_strength = 5

def heal_player():
    global player_health
    heal_amount = random.randint(10, 20)
    player_health += heal_amount
    print(f"{player_name} зібрав аптечку та відновив {heal_amount} здоров'я.")

while True:
    print(f"{player_name}: {player_health} здоров'я.")
    print(f"{enemy_name}: {enemy_health} здоров'я.")

    # Гравець вибирає дію
    action = input("Що будемо робити? (атакувати/зібрати аптечку/втекти): ")

    if action == "атакувати":
        player_damage = random.randint(1, player_strength)
        enemy_health -= player_damage
        print(f"{player_name} атакує {enemy_name} і завдає {player_damage} урону.")
        if enemy_health <= 0:
            print("Ви перемогли!")
            break

        enemy_damage = random.randint(1, enemy_strength)
        player_health -= enemy_damage
        print(f"{enemy_name} атакує {player_name} і завдає {enemy_damage} урону.")
        if player_health <= 0:
            print("Ви програли.")
            break
    elif action == "зібрати аптечку":
        heal_player()
    elif action == "Втекти":
        print("Ви втікаєте з бою.")
        break
    else:
        print("Невідома дія. Спробуйте ще раз.")
