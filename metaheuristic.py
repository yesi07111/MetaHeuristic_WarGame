import random
import subprocess
import sys
from typing import List
from metawars_api import Unit, army_cost
from goal_function import generate_target_armies

try:
    import rust_simulator
except ImportError:
    print("Compiling Rust module...")
    subprocess.run([
        sys.executable, "-m", "maturin", "develop", "--release"
    ], check=True)
    import rust_simulator

class GeneticAlgorithm:
    """Implementa un algoritmo genético para optimizar ejércitos en Meta Wars.
    
    Args:
        pop_size (int): Tamaño de la población. Default: 50
        elite_size (int): Número de elites a preservar. Default: 5
        mutation_rate (float): Probabilidad de mutación (0-1). Default: 0.1
        generations (int): Número de generaciones. Default: 100
    
    Attributes:
        target_armies (List[List[dict]]): Ejércitos objetivo serializados
    """
    def __init__(self, pop_size=50, elite_size=5, mutation_rate=0.1, generations=100):
        self.pop_size = pop_size
        self.elite_size = elite_size
        self.mutation_rate = mutation_rate
        self.generations = generations
        self.target_armies = self.serialize_targets()

    def serialize_army(self, army: List[Unit]) -> List[dict]:
        """Serializa un ejército para compatibilidad con Rust.
        
        Args:
            army (List[Unit]): Lista de unidades a serializar
            
        Returns:
            List[dict]: Lista de diccionarios con stats de las unidades
        """
        return [{
            "unit_type": u.unit_type,
            "weapon": u.weapon,
            "armour": u.armour,
            "level": u.level,
            "name": u.name,
            "attack": u.attack,
            "min_damage": u.min_damage,
            "max_damage": u.max_damage,
            "defense": u.defense,
            "hit_points": u.hit_points,
            "speed": u.speed,
            "atk_range": u.atk_range
        } for u in army]

    def rank_armies(self, population: List[List[Unit]]):
        """Evalúa la aptitud de los ejércitos contra objetivos.
        
        Args:
            population (List[List[Unit]]): Lista de ejércitos candidatos
            
        Returns:
            List[Tuple[List[Unit], int]]: Lista ordenada de (ejército, puntuación)
        """
        serialized = [self.serialize_army(army) for army in population]
        fitness_scores = rust_simulator.evaluate_armies(serialized, self.target_armies)
        return sorted(zip(population, fitness_scores), key=lambda x: x[1], reverse=True)
        
    def initial_population(self, num_individuals) -> List[List[Unit]]:
        """Genera población inicial aleatoria dentro del presupuesto.
        
        Args:
            num_individuals (int): Número de ejércitos a generar
            
        Returns:
            List[List[Unit]]: Población inicial válida
        """
        population = []
        for _ in range(num_individuals):
            army = []
            while army_cost(army) < 100000:
                unit_type = random.choice(Unit.UNITY_TYPES)
                weapon = random.choice(Unit.WEAPON_TYPES)
                armour = random.choice(Unit.ARMOUR_TYPES)
                level = random.randint(1, 20)
                army.append(Unit(unit_type, weapon, armour, level))
            population.append(army)
        return population

    def breed(self, parent1, parent2):
        """Cruza dos ejércitos usando single-point crossover.
        
        Args:
            parent1 (List[Unit]): Primer padre
            parent2 (List[Unit]): Segundo padre
            
        Returns:
            List[Unit]: Ejército hijo resultante
        """
        split = random.randint(0, min(len(parent1), len(parent2)))
        return parent1[:split] + parent2[split:]

    def mutate(self, army: List[Unit]) -> List[Unit]:
        """Aplica mutación aleatoria a un ejército.
        
        Args:
            army (List[Unit]): Ejército a mutar
            
        Returns:
            List[Unit]: Ejército mutado (puede ser inválido)
        """
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(army)-1)
            unit = army[idx]
            new_unit = Unit(
                unit_type=random.choice(Unit.UNITY_TYPES),
                weapon=random.choice(Unit.WEAPON_TYPES),
                armour=random.choice(Unit.ARMOUR_TYPES),
                level=unit.level + random.randint(-2, 2)
            )
            army[idx] = new_unit
        return army

    def evolve(self, ranked_population):
        """Genera nueva población mediante selección y operadores genéticos.
        
        Args:
            ranked_population (List[Tuple[List[Unit], int]]): Población ordenada
            
        Returns:
            List[List[Unit]]: Nueva población
        """
        elites = [x[0] for x in ranked_population[:self.elite_size]]
        
        children = []
        while len(children) < self.pop_size - self.elite_size:
            parent1, parent2 = random.choices(ranked_population[:10], k=2)
            child = self.breed(parent1[0], parent2[0])
            child = self.mutate(child)
            if army_cost(child) <= 100000:
                children.append(child)
        return elites + children

    def serialize_targets(self):
        """Serializa los ejércitos objetivo para Rust.
        
        Returns:
            List[List[dict]]: Ejércitos en formato serializado
        """
        return [
            [unit.__dict__ for unit in army]
            for army in generate_target_armies()
        ]

def generate_best_army(iterations=100, pop_size=50):
    """Ejecuta el algoritmo genético para encontrar el mejor ejército.
    
    Args:
        iterations (int): Número de generaciones. Default: 100
        pop_size (int): Tamaño de la población. Default: 50
        
    Returns:
        List[Unit]: Ejército optimizado
    """
    ga = GeneticAlgorithm(pop_size=pop_size)
    population = ga.initial_population(pop_size)
    
    for _ in range(iterations):
        ranked = ga.rank_armies(population)
        population = ga.evolve(ranked)
    
    return max(population, key=lambda x: x[1])[0]