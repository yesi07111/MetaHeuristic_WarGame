use pyo3::prelude::*;
use serde::{Deserialize, Serialize};
use rayon::prelude::*;
use rand::{Rng, thread_rng};

/// Representación serializable de una unidad para simulación en Rust
#[derive(Serialize, Deserialize, Debug, Clone, PartialEq)]
#[serde(rename_all = "snake_case")]
pub struct PyUnit {
    /// Tipo de unidad (ej: "archer", "knight")
    pub unit_type: String,
    /// Tipo de arma equipada
    pub weapon: String,
    /// Tipo de armadura equipada
    pub armour: String,
    /// Nivel de la unidad (≥1)
    pub level: u32,
    /// Nombre identificador
    pub name: String,
    /// Valor de ataque calculado
    pub attack: f64,
    /// Daño mínimo por ataque
    pub min_damage: f64,
    /// Daño máximo por ataque
    pub max_damage: f64,
    /// Valor de defensa calculado
    pub defense: f64,
    /// Puntos de vida actuales
    pub hit_points: f64,
    /// Velocidad para orden de ataque
    pub speed: f64,
    /// Rango de ataque máximo
    pub atk_range: f64,
}

/// Evalúa múltiples ejércitos contra todos los objetivos en paralelo
///
/// # Arguments
/// * `py_armies` - Lista de ejércitos candidatos a evaluar
/// * `target_armies` - Lista de ejércitos objetivo
///
/// # Returns
/// Vector con número de victorias por cada ejército candidato
#[pyfunction]
fn evaluate_armies(py_armies: &str, target_armies: &str) -> PyResult<Vec<u32>> {
    let py_armies: Vec<Vec<PyUnit>> = serde_json::from_str(py_armies)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid army JSON: {}", e)))?;
    
    let target_armies: Vec<Vec<PyUnit>> = serde_json::from_str(target_armies)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyValueError, _>(format!("Invalid target JSON: {}", e)))?;

    let results: Vec<u32> = py_armies
        .par_iter()
        .map(|army| {
            target_armies.par_iter()
                .map(|target| simulate_battle(army, target))
                .sum()
        })
        .collect();
    
    Ok(results)
}

/// Simula una batalla completa entre dos ejércitos
///
/// # Arguments
/// * `army` - Ejército aliado
/// * `target` - Ejército enemigo
///
/// # Returns
/// 1 si gana el ejército aliado, 0 en caso contrario
fn simulate_battle(army: &[PyUnit], target: &[PyUnit]) -> u32 {
    let mut left: Vec<PyUnit> = army.to_vec();
    let mut right: Vec<PyUnit> = target.to_vec();
    let mut rng = thread_rng();

    while !left.is_empty() && !right.is_empty() {
        // Generar orden de ataque considerando solo unidades vivas
        let mut attack_order: Vec<(PyUnit, bool)> = left.iter()
            .filter(|u| u.hit_points > 0.0)
            .map(|u| (u.clone(), true))
            .chain(
                right.iter()
                    .filter(|u| u.hit_points > 0.0)
                    .map(|u| (u.clone(), false))
            )
            .collect();

        // Ordenar por velocidad descendente
        attack_order.sort_by(|a, b| b.0.speed.partial_cmp(&a.0.speed).unwrap());

        for (unit, is_left) in attack_order {
            let (allies, enemies) = if is_left {
                (&mut left, &mut right)
            } else {
                (&mut right, &mut left)
            };

            // Verificar si la unidad sigue viva y obtener su índice
            let Some(index) = allies.iter()
                .position(|u| u == &unit && u.hit_points > 0.0) else { continue };

            // Calcular rango efectivo corregido
            let allies_len = allies.len();
            let actual_range = (unit.atk_range - (allies_len - 1 + index) as f64).max(0.0) as usize;
            if actual_range == 0 || enemies.is_empty() { continue; }

            // Seleccionar defensor aleatorio dentro del rango
            let defender_idx = rng.gen_range(0..actual_range.min(enemies.len()));
            let defender = &mut enemies[defender_idx];

            // Resolver lógica de ataque
            let dice_roll = rng.gen_range(1..=20);
            if dice_roll == 1 { continue; }  // Fallo crítico

            let attack_value = unit.attack + dice_roll as f64;
            let defense_value = defender.defense + 20.0;

            if dice_roll != 20 && attack_value <= defense_value { continue; }

            // Calcular daño aplicado
            let damage = if dice_roll == 20 {
                rng.gen_range(unit.min_damage..=unit.max_damage) * 3.0
            } else {
                rng.gen_range(unit.min_damage..=unit.max_damage)
            };

            defender.hit_points -= damage;
        }

        // Eliminar unidades muertas de ambos bandos
        left.retain(|u| u.hit_points > 0.0);
        right.retain(|u| u.hit_points > 0.0);
    }

    if right.is_empty() { 1 } else { 0 }
}

/// Registra el módulo para Python
#[pymodule]
fn rust_simulator(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(evaluate_armies, m)?)?;
    Ok(())
}