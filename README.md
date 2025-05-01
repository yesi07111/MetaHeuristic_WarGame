# ⚔️ Meta Wars: Darwin's Army Simulator  
*"Survival of the fittest... engineered through evolution"* 🧬

## 📜 Rules of Engagement  
All battles follow `rules.pdf` - your holy grail for unit stats, combat mechanics, and budget limits (💰 Max 100,000 gold per army).  

## 🗃️ Project Structure  
```bash
├── compiled/           # 🦀 Prebuilt Rust wheels (no compiler needed!)
├── internal_data.json  # 📊 Unit stats & names (loaded automatically)
├── test_*_army.json    # 🧪 Sample armies (try modifying these!)
├── metawars_api.py     # 🎮 Combat engine with ROFL battle messages
├── metaheuristics.py   # 🧬 Genetic Algorithm mastermind
├── goal_function.py    # 🎯 Target armies to annihilate
└── main.py             # ⚡ Demo: Evolve army vs test opponents
```

## 🕹️ How to Play  
### 1. 🛠️ Create Your Army ⚔️
```python
# main.py example - Build your legion ✨
my_army = [
    Unit(Unit.knight, Weapon.diamond, Armour.steel, level=3),  # 🛡️
    Unit(Unit.archer, Weapon.wood, Armour.diamond, level=5)    # 🏹
]
```

### 2. 🔥 Simulate Battles 💥
```python
# Watch tactical carnage unfold 🍿🚀
results = simulation(my_army, enemy_army, verbose=True)

# Battle log snippet:
# "Sir Lancelot tried to cast fireball... set himself on fire 🔥"
```

## 🧪 Genetic Algorithm: Army Evolution 101  
**Darwin Mode Activated:**  
1. 🧬 **Population**: 50 random armies (each one within budget)  
2. 🏆 **Fitness**: Battles all target armies → Wins = Score  
3. 🥇 **Selection**: Keep top 5 elites + best 10% parents  
4. 🧬 **Crossover**: Mix units from two parents (single-point splice)  
5. 🧪 **Mutation**: 10% chance to randomly upgrade units  

*Powered by Rust ⚡: Simulates 1000x faster than Python!*

## 🎯 Target Armies (Goal Function)  
Your army must defeat these nightmares ☠️:  
```python
# goal_function.py
[
   124x Lv20 Diamond Peasants 🧑🌾,  # "Horde mode activated"
   24x Lv20 Uber-Swordmen ⚔️,       # "Walking meat grinders"
   386x Lv5 Spearmen 🛡️,            # "Pointy wall of death"
   ... # 6 more hellish combos
]
```

## 🚀 Quick Start Guide  
1. 📦 Install dependencies:  
```bash
pip install -r requirements.txt
```

2. 🧬 Run evolution demo:  
```bash
python main.py  # Watch super-soldiers emerge! 🚀
```

3. 🎯 Modify targets in `goal_function.py` for new challenges!  


## ☠️ Battle Royale Highlights  
- **Critical Fails**: "Tripped on own sword 🤦♂️"  
- **Epic Kills**: "Teleported into enemy camp 🌀→💀"  
- **Cheater Detection**: "Rabid bunnies ate the commander 🐇🔪"  

*Pro Tip: Run simulations with `verbose=True` for maximum entertainment!*  



