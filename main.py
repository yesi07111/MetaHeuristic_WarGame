from metawars_api import Unit, Weapon, Armour, army_cost, simulation
from metaheuristic import generate_best_army

test_left_army = generate_best_army(20, 10)

Unit.save_army(test_left_army, "./test_left_army.json")
test_left_army = Unit.load_army("./test_left_army.json")
print("Army cost:", army_cost(test_left_army))
print(*test_left_army, sep="\n")

test_right_army = [
    Unit(Unit.knight, Weapon.diamond, Armour.steel, level=3),
    Unit(Unit.swordman, Weapon.steel, Armour.wood, level=4),
    Unit(Unit.swordman, Weapon.steel, Armour.wood, level=3),
    Unit(Unit.archer, Weapon.diamond, Armour.wood, level=1),
    Unit(Unit.archer, Weapon.diamond, Armour.wood, level=2),
]

Unit.save_army(test_right_army, "./test_right_army.json")
test_right_army = Unit.load_army("./test_right_army.json")
print("Army cost:", army_cost(test_right_army))
print(*test_right_army, sep="\n")

simulation(test_left_army, test_right_army)
