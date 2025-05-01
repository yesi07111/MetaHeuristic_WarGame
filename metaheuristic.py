import json
import os
import random
import subprocess
import sys
from typing import List
from metawars_api import (
    Unit, 
    army_cost,
    UNITY_TYPES,  
    WEAPON_TYPES,  
    ARMOUR_TYPES   
)
from goal_function import generate_target_armies

def install_rust_module():
    """Instala el módulo Rust precompilado desde el wheel"""
    wheel_path = os.path.join(os.path.dirname(__file__), "compiled", "rust_simulator-0.1.0-cp311-none-win_amd64.whl")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "--force-reinstall", "--no-index", "--find-links", "compiled",
            "rust_simulator"
        ], check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Error instalando módulo Rust. Ejecuta manualmente:\n"
            f"pip install {wheel_path}"
        ) from e

try:
    import rust_simulator # type: ignore
except ImportError:
    install_rust_module()
    import rust_simulator # type: ignore

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
        # Serializar a JSON
        serialized = json.dumps([self.serialize_army(army) for army in population])
        target_armies = json.dumps(self.target_armies)
        
        # Llamar a Rust con JSON
        fitness_scores = rust_simulator.evaluate_armies(serialized, target_armies)
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
            max_attempts = 100  # Evitar bucles infinitos
            while army_cost(army) < 100000 and max_attempts > 0:
                new_unit = Unit(
                    unit_type=random.choice(UNITY_TYPES),
                    weapon=random.choice(WEAPON_TYPES),
                    armour=random.choice(ARMOUR_TYPES),
                    level=random.randint(1, 20)
                )
                if army_cost(army) + new_unit.cost <= 100000:
                    army.append(new_unit)
                max_attempts -= 1
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
        original_cost = army_cost(army)
    
        if random.random() < self.mutation_rate:
            idx = random.randint(0, len(army)-1)
            original_unit = army[idx]
            
            # Intentar máximo 10 mutaciones válidas
            for _ in range(10):
                new_level = max(1, original_unit.level + random.randint(-2, 2))
                new_level = min(new_level, 20)
                
                new_unit = Unit(
                    unit_type=random.choice(UNITY_TYPES),
                    weapon=random.choice(WEAPON_TYPES),
                    armour=random.choice(ARMOUR_TYPES),
                    level=new_level
                )
                
                # Calcular nuevo costo
                new_cost = original_cost - original_unit.cost + new_unit.cost
                if new_cost <= 100000:
                    army[idx] = new_unit
                    break
                    
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
        max_attempts = 1000  # Prevenir bucles infinitos
        while len(children) < self.pop_size - self.elite_size and max_attempts > 0:
            parent1, parent2 = random.choices(ranked_population[:10], k=2)
            child = self.breed(parent1[0], parent2[0])
            child = self.mutate(child)
            
            # Validación estricta de costo
            total_cost = army_cost(child)
            if total_cost <= 100000 and total_cost > 0:  # Ejército no vacío
                children.append(child)
            max_attempts -= 1
        
        return elites + children

    def serialize_targets(self):
        """Serializa los ejércitos objetivo para Rust.
        
        Returns:
            List[List[dict]]: Ejércitos en formato serializado
        """
        return [
            [{
                "unit_type": unit.unit_type,
                "weapon": unit.weapon,
                "armour": unit.armour,
                "level": unit.level,
                "name": unit.name,
                "attack": unit.attack,
                "min_damage": unit.min_damage,
                "max_damage": unit.max_damage,
                "defense": unit.defense,
                "hit_points": unit.hit_points,
                "speed": unit.speed,
                "atk_range": unit.atk_range
            } for unit in army]
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
    
    best_army = None
    best_score = -1
    
    for _ in range(iterations):
        ranked = ga.rank_armies(population)  # Lista de (army, fitness)
        current_best_army, current_best_score = ranked[0]
        
        if current_best_score > best_score:
            best_army = current_best_army
            best_score = current_best_score
            
        population = ga.evolve(ranked)
    
    return best_army