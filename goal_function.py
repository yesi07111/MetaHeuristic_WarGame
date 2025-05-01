import copy
from metawars_api import Unit, Weapon, Armour, army_cost, simulation


def generate_target_armies():
    armies = []

    peasant_army = [Unit(Unit.peasant, Weapon.diamond,
                         Armour.diamond, level=20) for i in range(124)]
    assert(army_cost(peasant_army) <= 100000)
    armies.append(peasant_army)

    swordman_army = [Unit(Unit.swordman, Weapon.diamond,
                          Armour.diamond, level=20) for i in range(24)]
    assert(army_cost(swordman_army) <= 100000)
    armies.append(swordman_army)

    spearman_army = [Unit(Unit.spearman, Weapon.diamond,
                          Armour.diamond, level=5) for i in range(386)]
    assert(army_cost(spearman_army) <= 100000)
    armies.append(spearman_army)

    archer_army = [Unit(Unit.archer, Weapon.diamond,
                        Armour.diamond, level=4) for i in range(386)]
    assert(army_cost(archer_army) <= 100000)
    armies.append(archer_army)

    defender_army = [Unit(Unit.defender, Weapon.diamond,
                          Armour.diamond, level=20) for i in range(12)]
    assert(army_cost(defender_army) <= 100000)

    horseman_army = [Unit(Unit.horseman, Weapon.diamond,
                          Armour.diamond, level=10) for i in range(49)]
    assert(army_cost(horseman_army) <= 100000)

    sniper_army = [Unit(Unit.sniper, Weapon.diamond,
                        Armour.diamond, level=2) for i in range(613)]
    assert(army_cost(sniper_army) <= 100000)

    knight_army = [Unit(Unit.knight, Weapon.diamond,
                        Armour.diamond, level=15) for i in range(11)]
    assert(army_cost(knight_army) <= 100000)

    elefant_army = [Unit(Unit.elefant, Weapon.diamond,
                         Armour.diamond, level=8) for i in range(19)]
    assert(army_cost(elefant_army) <= 100000)

    return armies


def get_army_fitness(army):
    assert(army_cost(army) <= 100000)
    number_of_wins = 0
    target_armies = generate_target_armies()
    for target_army in target_armies:
        cpy_army = copy.deepcopy(army)
        cpy_target_army = copy.deepcopy(target_army)
        len_cpy_army, len_cpy_target_army = simulation(
            cpy_army, cpy_target_army, False)
        if len_cpy_target_army == 0 and len_cpy_army > 0:
            number_of_wins += 1
    return number_of_wins
