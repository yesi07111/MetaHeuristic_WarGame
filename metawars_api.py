from __future__ import annotations

import json
from pathlib import Path
from typing import List, Union
import random
import time

def load_internal_data() -> dict:
    with open("internal_data.json", "r", encoding="utf-8") as data_fd:
        return json.load(data_fd)


DATA = load_internal_data()

UNITS_DATA = DATA["units"]
WEAPON_DATA = DATA["weapon"]
ARMOUR_DATA = DATA["armour"]
NAMES_DATA=DATA["names"]

UNITY_TYPES = list(UNITS_DATA.keys())
WEAPON_TYPES = list(list(WEAPON_DATA.values())[0].keys())
ARMOUR_TYPES = list(list(ARMOUR_DATA.values())[0].keys())
UNIT_NAMES = list(NAMES_DATA.values())

DEATHS = [ 
"was cut in two pieces", 
"tripped on their own sword and impaled themselves", 
"mistook a dragon for a friendly ally", 
"got lost in their own castle and starved to death", 
"tried to cast a fireball spell but set themselves on fire instead", 
"ate a poisonous mushroom thinking it was a magical potion", 
"challenged a troll to a tickling contest and was squashed", 
"accidentally stepped into a teleportation portal and ended up in the enemy's camp", 
"tried to ride a unicorn but got kicked into oblivion", 
"fell into a pit trap filled with rabid bunnies", 
"decided to juggle live grenades and failed spectacularly", 
"choked on a turkey leg during a victory feast", 
"slipped on a banana peel and fell into a moat filled with crocodiles", 
"insulted a powerful wizard who turned them into a chicken", 
"tried to bribe the enemy with counterfeit gold and was promptly executed", 
"thought they were invisible after drinking an invisibility potion, but they weren't", 
"decided to take a nap on the battlefield and was mistaken for a fallen soldier", 
"tried to negotiate a peace treaty with a horde of bloodthirsty goblins", 
"accidentally triggered their own booby trap", 
"got tangled in their own chainmail and couldn't escape", 
"ate a cursed apple and fell into an eternal slumber", 
"thought they were invincible after drinking a potion of invulnerability, but it was just grape juice", 
"tried to impress their crush by jousting blindfolded and impaled themselves on a tree", 
"fell into a pit of quicksand and sank while reciting a heroic monologue", 
"tried to tame a wild griffin but ended up as its lunch", 
"danced too vigorously during a victory celebration and fell off a cliff", 
"attempted to behead a zombie but their sword got stuck in its neck", 
"tried to cast a lightning spell during a thunderstorm and was struck by real lightning", 
"fell asleep on watch duty and woke up surrounded by enemy soldiers", 
"tried to ride a wyvern but accidentally pulled its tail and got incinerated", 
"ate a cursed pie and turned into a talking squirrel", 
"thought they could fly after drinking a levitation potion and jumped off a tower", 
"got entangled in their own catapult and launched themselves into the enemy lines", 
"tried to use a magic wand but accidentally turned themselves into a toad", 
"slipped on a banana peel and fell into a pit of hungry wolves", 
"tried to play dead to trick the enemy but ended up being buried alive", 
"thought they could breathe underwater and drowned in a shallow pond", 
"tried to tame a ferocious warhorse but got dragged across the battlefield instead", 
"tripped over their own beard and fell off a cliff", 
"attempted to use a cursed sword and was instantly turned into a statue", 
"tried to use a cursed mirror and got trapped inside it forever", 
"thought they could communicate with animals and was devoured by a pack of wolves", 
"tried to sneak into the enemy camp disguised as a sheep but was mistaken for dinner", 
"got lost in a maze of their own design and starved to death", 
"thought they could control the weather and summoned a lightning storm that struck them down", 
"tried to impress their comrades with a daring acrobatic maneuver but ended up impaled on a flagpole", 
"ate a magical mushroom and grew so tall that they couldn't fit through the castle gates", 
"tried to use a cursed amulet and was cursed with eternal bad luck", 
"thought they could outrun a charging rhinoceros but ended up as a pancake", 
"tried to capture a basilisk but was turned to stone by its deadly gaze", 
"attempted to tame a wild dragon but ended up as its snack", 
"thought they could communicate with trees and was crushed by a falling oak", 
"got their foot stuck in a bear trap and couldn't escape", 
"tried to use a cursed compass and ended up wandering in circles for eternity", 
"thought they could outdrink a group of dwarves and succumbed to alcohol poisoning", 
"tried to swim across a river infested with piranhas", 
"thought they could outsmart a group of cunning goblins but fell into their own trap", 
"got their head stuck in a suit of armor and suffocated", 
"tried to tame a wild centaur but got trampled instead", 
"thought they could outdance a group of enchanted skeletons but ended up as a pile of bones", 
"ate a cursed sandwich and turned into a talking donkey", 
"tried to use a cursed ring and became invisible forever", 
"thought they could outwit a group of witches but ended up as a frog", 
"got their beard caught in a catapult and was launched into the enemy lines", 
"tried to tame a pack of wild wolves but became their dinner instead", 
"thought they could outmaneuver a group of skilled archers but ended up as a pincushion", 
"ate a cursed chocolate and turned into a giant marshmallow", 
"tried to use a cursed book and was sucked into its pages", 
"thought they could outsmart a group of mischievous fairies but ended up as their plaything", 
"got their foot stuck in a giant Venus flytrap and became its meal", 
"tried to tame a wild minotaur but got trampled by its hooves", 
"thought they could outswim a group of mermaids but drowned in the process", 
"ate a cursed cookie and turned into a living gingerbread man", 
"tried to use a cursed staff and was transformed into a statue", 
"thought they could outwit a group of clever trolls but ended up as their bridge",
"got their arm stuck in a dragon's hoard and was burned to a crisp", 
"tried to tame a swarm of angry bees but got stung to death", 
"thought they could outplay a group of mischievous imps but ended up as their eternal entertainment", 
"ate a cursed candy and turned into a talking skeleton", 
"tried to use a cursed potion and was transformed into a giant slug", 
"thought they could outrun a group of enchanted forest animals but got trampled by a stampede", 
"got their hand stuck in a giant venus flytrap and was slowly digested", 
"tried to tame a wild chimera but got devoured by its fiery breath", 
"thought they could outsmart a group of clever sphinxes but failed their riddles and met a gruesome fate", 
"ate a cursed cupcake and turned into a living statue", 
"tried to use a cursed scroll and was transported to a realm of eternal darkness", 
"thought they could outmaneuver a group of cunning harpies but ended up as their meal", 
"got their foot stuck in a giant clam and drowned as the tide came in", 
"tried to tame a pack of wild hyenas but became their prey instead", 
"thought they could outwit a group of trickster leprechauns but ended up as their servant", 
"ate a cursed ice cream and turned into a frozen statue", 
"tried to use a cursed talisman and was trapped in a never-ending nightmare", 
"thought they could outplay a group of mischievous pixies but ended up as their plaything", 
"got their head stuck in a giant pitcher plant and was slowly dissolved", 
"tried to tame a wild basilisk but was turned to stone by its deadly gaze", 
"thought they could outsmart a group of cunning sirens but drowned in their enchanting song", 
"ate a cursed donut and turned into a living jelly", 
"tried to use a cursed artifact and was banished to a realm of eternal torment", 
"thought they could outrun a group of lightning-fast sprites but was zapped into oblivion",
"got their foot stuck in quicksand and sank to their demise", 
"tried to tame a wild manticore but got impaled by its poisonous tail", 
"thought they could outwit a group of clever gnomes but ended up as their garden ornament", 
"ate a cursed pizza and turned into a living statue", 
"tried to use a cursed relic and was trapped in a dimension of eternal chaos", 
"thought they could outmaneuver a group of cunning gremlins but ended up as their mechanical plaything", 
"got their head stuck in a giant pitcher plant and suffocated", 
"tried to tame a pack of wild jackals but became their prey instead", 
"thought they could outsmart a group of clever kobolds but ended up as their prisoner", 
"ate a cursed burger and turned into a living slime", "tried to use a cursed totem and was cursed with it", 
"was tickled to death by enemy soldiers", "was poked to death with a foam sword", 
"died from laughter after being insulted by the enemy", 
"was defeated by a deadly game of rock-paper-scissors", 
"was smothered to death by a barrage of feather pillows", 
"was defeated by a fierce tickle fight", 
"tripped over their own shoelaces and was trampled by the enemy", 
"was defeated in a thumb war", 
"was scared to death by the enemy's silly faces", 
"was defeated by a group of enemy soldiers armed with rubber chickens", 
"was tickled by a feather until they couldn't breathe", 
"was defeated by a surprise attack of enemy soldiers armed with rubber ducks", 
"was defeated in a game of medieval charades and died of embarrassment", 
"was defeated by an enemy who couldn't stop telling bad jokes", 
"was defeated by a group of enemy soldiers armed with whoopee cushions", 
"was outsmarted by the enemy in a game of medieval trivia", 
"was defeated by an enemy who used a rubber chicken as a weapon", 
"was defeated in a game of medieval hopscotch and fell into a pit of doom", 
"was defeated by a group of enemy soldiers armed with silly string", 
"was defeated by an enemy who had an unstoppable dance-off", 
"was defeated in a game of medieval musical chairs and was left behind", 
"was defeated by an enemy who used a banana peel as a weapon", 
"was defeated in a game of medieval limbo and couldn't get back up", 
"was defeated by a group of enemy soldiers armed with water balloons", 
"was defeated by an enemy who had an unbeatable game of medieval charades", 
"was defeated in a game of medieval Simon Says and couldn't stop", 
"was defeated by an enemy who used a whoopee cushion as a weapon", 
"was defeated in a game of medieval hide-and-seek and was never found", 
"was defeated by a group of enemy soldiers armed with rubber spiders", 
"was defeated by an enemy who had an unstoppable game of medieval tag", 
"was defeated in a game of medieval musical chairs and was left without a seat", 
"was defeated by an enemy who used a rubber chicken as a boomerang", 
"was defeated in a game of medieval hopscotch and stepped on the wrong square", 
"was defeated by a group of enemy soldiers armed with water guns", 
"was defeated by an enemy who had an unbeatable game of medieval trivia", 
"was defeated by an enemy who used a banana peel as a trap", 
"was defeated by an enemy who had an unbeatable game of medieval tag", 
"was defeated by an enemy who had an unstoppable game of medieval trivia", 
"was tickled to death by an enemy knight",
"was defeated by a deadly staring contest",
"was smothered to death by a rain of cotton candy",
"was trampled by their own army during a dance-off",
"was defeated by a horde of angry bunnies",
"died from a paper cut inflicted by a love letter",
"was mistaken for a scarecrow and pecked to death by crows",
"was defeated by a group of knights armed with rubber chickens",
"was crushed under the weight of their own armor while sneezing",
"was outsmarted by a cunning enemy squirrel",
"died from a heart attack caused by a surprise birthday party",
"was defeated by a deadly game of thumb wars",
"was suffocated by an enemy wizard's never-ending fart spell",
"was accidentally swallowed by a dragon while trying to slay it",
"was defeated by a troop of enemy clowns armed with water balloons",
"was struck by lightning while trying to take a selfie during a storm",
"was defeated by a relentless army of killer kittens",
"died from laughter after hearing a particularly bad joke from the enemy",
"was hypnotized by an enemy magician and danced themselves to death",
"was defeated by a troop of enemy knights armed with whoopee cushions",
"was crushed by a falling piano dropped by an enemy catapult",
"was defeated in a medieval rap battle and died of embarrassment",
"died from a severe allergic reaction to flowers thrown by admirers",
"was defeated by an enemy with a deadly weaponized feather duster",
"was accidentally swallowed by a giant whale during a naval battle",
"was defeated by a group of enemy jesters armed with exploding pies",
"died from a severe case of food poisoning after eating enemy rations",
"was defeated by an army of enemy musicians armed with bagpipes",
"was turned into a frog by an enemy sorcerer and couldn't change back",
"was defeated by an enemy knight armed with a rubber chicken",
"was accidentally catapulted into the enemy camp and mistaken for a spy",
"was defeated by an enemy archer with a deadly barrage of marshmallows",
"died from a severe case of helmet hair that caused a fatal distraction",
"was defeated by a troop of enemy jesters armed with exploding confetti",
"was trampled to death by a stampede of enemy unicorns",
"was defeated by an enemy sorcerer who turned their sword into a banana",
"was crushed by a giant rolling cheese wheel during a siege",
"died from a fatal allergic reaction to their own suit of armor",
"was defeated by a group of enemy knights armed with rubber chickens",
"was accidentally swallowed by a dragon while trying to negotiate peace",
"was defeated by an army of enemy musicians armed with kazoos",
"was struck by a flying cow launched by an enemy trebuchet",
"was defeated by an enemy knight who tickled them into submission",
"died from a fatal case of stage fright during a battle speech",
"was defeated by an enemy with a deadly weaponized feather boa",
"was crushed under the weight of their own armor while attempting a cartwheel",
"was defeated by a group of enemy archers armed with rubber bands",
"died from an unfortunate encounter with a cursed fortune cookie",
"was defeated by an enemy sorcerer who turned their horse into a frog",
"was accidentally swallowed by a giant snake during a reconnaissance mission",
"was defeated by an army of enemy jesters armed with exploding balloons",
"died from an extreme case of sunburn after forgetting to wear sunscreen",
"was defeated by an enemy knight who challenged them to a dance-off",
"was crushed by a falling anvil dropped by an enemy airship",
"was defeated by a troop of enemy musicians armed with accordions",
"died from a severe case of food poisoning after eating enemy jester pies",
"was defeated by an enemy knight who defeated them in a game of chess"]

class Weapon:
    wood = "wood"
    steel = "steel"
    diamond = "diamond"


class Armour:
    wood = "wood"
    steel = "steel"
    diamond = "diamond"


WPN_MULT = {
    Weapon.wood: 1.2,
    Weapon.steel: 1.6,
    Weapon.diamond: 2.0,
}

DEF_MULT = {
    Armour.wood: 1.2,
    Armour.steel: 1.6,
    Armour.diamond: 2.0,
}


class Unit:
    peasant = "peasant"
    swordman = "swordman"
    spearman = "spearman"
    archer = "archer"
    defender = "defender"
    horseman = "horseman"
    sniper = "sniper"
    knight = "knight"
    elefant = "elefant"

    def __init__(self, unit_type: str, weapon: str, armour: str, level: int, name=""):
        assert unit_type in UNITY_TYPES, f"Invalid unit type '{unit_type}'"
        assert weapon in WEAPON_TYPES, f"Invalid weapon type '{weapon}'"
        assert armour in ARMOUR_TYPES, f"Invalid armour type '{armour}'"
        assert level > 0, "Level must be greater than 1"

        self.unit_type = unit_type
        self.weapon = weapon
        self.armour = armour
        self.level = level
        self.name = name

        unit_data = UNITS_DATA[unit_type]
        self.weapon_cost = WEAPON_DATA[unit_type][weapon]
        self.armour_cost = ARMOUR_DATA[unit_type][weapon]
        self.unit_cost = unit_data["cost"] * (level**2)

        if(name == ""):
            self.name = UNIT_NAMES[random.randint(0, len(UNIT_NAMES) -1)]
        else:
            self.name = name

        self.cost = self.unit_cost + self.armour_cost + self.unit_cost

        self.attack = unit_data["atk"] * WPN_MULT[weapon] * (1.2**level)
        self.min_damage = unit_data["dmg"][0] * (1.2**level)
        self.max_damage = unit_data["dmg"][1] * (1.2**level)
        self.defense = unit_data["def"] * DEF_MULT[armour] * (1.2**level)
        self.hit_points = unit_data["hp"] * (1.2**level)
        self.speed = unit_data["spd"] * (1.2**level)
        self.atk_range = unit_data["ran"]

    def __repr__(self) -> str:
        return (
            f"{self.name} -> ({self.unit_type}, cost={self.cost}, atk={self.attack}, "
            f"dmg={self.min_damage}-{self.max_damage}, def={self.defense}, "
            f"hp={self.hit_points}, spd={self.speed}, rng={self.atk_range})"
        )

    def __str__(self) -> str:
        return repr(self)

    def clone(self) -> Unit:
        return Unit(
            unit_type=self.unit_type,
            weapon=self.weapon,
            armour=self.armour,
            level=self.level,
        )

    @staticmethod
    def load_army(path: Union[str, Path]) -> List[Unit]:
        path = Path(path) if isinstance(path, str) else path

        if not path.exists() or not path.is_file():
            raise ValueError("Invalid army file path")

        if path.suffix != ".json":
            raise ValueError("Invalid army file type")

        with open(path, "r", encoding="utf-8") as army_fd:
            army_data = json.load(army_fd)

        army: List[Unit] = []

        for unit in army_data:
            army.append(
                Unit(
                    unit_type=unit["unit_type"],
                    weapon=unit["weapon"],
                    armour=unit["armour"],
                    level=unit["level"],
                    name=unit["name"]
                )
            )

        return army

    @staticmethod
    def save_army(army: List[Unit], path: Union[str, Path]):
        data = [
            dict(
                unit_type=unit.unit_type,
                weapon=unit.weapon,
                armour=unit.armour,
                level=unit.level,
                name=unit.name,
            )
            for unit in army
        ]
        with open(path, "w+", encoding="utf-8") as data_fd:
            json.dump(data, data_fd, indent=4, ensure_ascii=False)


def army_cost(army: List[Unit]) -> int:
    return sum(unit.cost for unit in army)

def sprint(text, verbose):
    if verbose:
        print(text)

def simulation(left_army: List[Unit], right_army: List[Unit], verbose=True, timeout = None):
    # Seeing if the mony is OK
    sprint("\n\n Starting simulation", verbose)
    left_cost = army_cost(left_army)
    right_cost =  army_cost(right_army)
    if(left_cost > 100000 or right_cost > 100000):
        if (left_cost > 100000 and right_cost > 100000):
            sprint("Both commanders are shameless. The soldiers return home disappointed that they have not been able to cut off a single head.", verbose)
            return 0
        else:
            if(right_cost > left_cost ):
                cheater = "right"
                result = 1
            else:
                cheater = "left"
                result = 2
            sprint(f"The commander of the {cheater} army is a cheater. Soldiers return home disappointed that they were not able to stab anyone to death", verbose)
            return result
    

    # Lets simulate
    start_time = time.time()
    while(len(left_army) > 0 and len(right_army) > 0):
        current_time = time.time() - start_time
        if timeout and current_time > timeout:
            return (len(left_army), len(right_army))
        
        sprint("+++++++++++++++++++++++++++++++++++++++++", verbose)
        attack_order = sorted(left_army + right_army, key=lambda u: u.speed, reverse=True)

        for unit in attack_order:
            if(len(right_army) <= 0 or len(left_army) <= 0):
                break
            if(unit.hit_points <= 0):
                continue
            
            if(unit in left_army):
                enemy = right_army
                allies = left_army
            else:
                enemy = left_army
                allies = right_army
            actual_range = unit.atk_range - (len(allies) -1 + allies.index(unit))
            if(actual_range <= 0):
                sprint(f"{unit.name} couldn't attack because the idiot was out of range ", verbose)
                continue

            actual_range = min(actual_range, len(enemy)-1)

            defender = enemy[random.randint(0, actual_range)]
            attacker = unit

            # Let's fight!
            target = defender.defense + 20
            throw = random.randint(0, 20)
            if(throw == 1):
                sprint("CRITICAL MISS!", verbose)
                sprint(f"{unit.name} misses", verbose)
                continue

            if(throw == 20):
                sprint("CRITICAL HIT!", verbose)

            if(throw + attacker.attack < target and throw != 20):
                sprint(f"{unit.name} misses", verbose)
                continue

            # The attack was a hit! 
            damage = random.randint(int(unit.min_damage), int(unit.max_damage))
            if (throw == 20):
                damage = damage*3
            sprint(f"{attacker.name} landed an attack on {defender.name} and dealt [{damage}] damage!", verbose)
            defender.hit_points -= damage
            if(defender.hit_points <= 0):
                sprint(f"{defender.name} {DEATHS[random.randint(0, len(DEATHS) - 1)]}", verbose)
                enemy.remove(defender)

        sprint(f"Round results: left army {len(left_army)} - {len(right_army)} right army", verbose)
        sprint("+++++++++++++++++++++++++++++++++++++++++", verbose)
    
    sprint(f"Final results: left army {len(left_army)} - {len(right_army)} right army", verbose)
    return (len(left_army), len(right_army))





def tu_funcion_con_timeout(tiempo_limite):
    inicio = time.time()
    tiempo_actual = 0

    while tiempo_actual < tiempo_limite:
        # Tu lógica aquí
        tiempo_actual = time.time() - inicio

        # Si tu condición de salida se cumple, puedes romper el bucle
        if condicion_de_salida():
            break