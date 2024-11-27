import numpy as np
from collections import Counter

rand = np.random.default_rng()
DOMAIN = 'Domain'
STRONGBOX = 'Strongbox'

SET = 'Set'
SLOT = 'Slot'
MAIN_STAT = 'Main Stat'
STARTING_SUBSTATS = 'Starting Substats'
SUBSTATS = 'Substats'
ROLLS = 'Rolls'
ROLL_LEVEL = 'Roll Level'
WANTED = 'Wanted'

slots = ['Flower', 'Feather', 'Sands', 'Goblet', 'Circlet']
main_stat_probabilities = {
    'Flower': {'HP': 1},
    'Feather': {'ATK': 1},
    'Sands': {'HP%': 0.2668, 'ATK%': 0.2666, 'DEF%': 0.2666, 'ER': 0.1, 'EM': 0.1},
    'Goblet': {'HP%': 0.1925, 'ATK%': 0.1925, 'DEF%': 0.19, 'Pyro': 0.05, 'Electro': 0.05, 'Cryo': 0.05,
               'Hydro': 0.05, 'Dendro': 0.05, 'Anemo': 0.05, 'Geo': 0.05, 'Physical': 0.05, 'EM': 0.025},
    'Circlet': {'HP%': 0.22, 'ATK%': 0.22, 'DEF%': 0.22, 'CR': 0.1, 'CD': 0.1, 'Healing': 0.1, 'EM': 0.04}
}
num_of_substats_probabilities = {
    'Domain': {3: 0.8, 4: 0.2},
    'Strongbox': {3: 0.66, 4: 0.34}
}
substats_weights = {'HP': 6, 'ATK': 6, 'DEF': 6, 'HP%': 4, 'ATK%': 4, 'DEF%': 4, 'ER': 4, 'EM': 4, 'CR': 3, 'CD': 3}
substat_max_rolls = {'HP': 298.75, 'ATK': 19.45, 'DEF': 23.15, 'HP%': 5.83, 'ATK%': 5.83, 'DEF%': 7.29, 'EM': 23.31,
                     'ER': 6.48, 'CR': 3.89, 'CD': 7.77}

def generate_substats(artifact: dict):
    main_stat = artifact.get(MAIN_STAT)
    substats = artifact.get(SUBSTATS)
    rolls = artifact.get(ROLLS)
    roll_level = artifact.get(ROLL_LEVEL)

    for i in range(4):
        remaining_substats = [key for key in substats_weights if key not in substats and key != main_stat]
        substat_key_sum = sum(substats_weights[key] for key in remaining_substats)
        substat_probabilities = [substats_weights[key] / substat_key_sum for key in remaining_substats]
        generated_substat = rand.choice(remaining_substats, p=substat_probabilities)
        substats.append(generated_substat)
        rolls.append(i+1)
        roll_level.append(roll_substat())

def roll_substat() -> float:
    return rand.choice([0.7, 0.8, 0.9, 1])

def select_main_stat(slot: str) -> str:
    probabilities = main_stat_probabilities[slot]
    return rand.choice(list(probabilities.keys()), p=list(probabilities.values()))

def check_wanted(current, wanted):
    if wanted is not None and current != wanted:
        return True
    else:
        return False

def generate_artifact(source: str, wanted:dict = None) -> dict:
    set_wanted = wanted.get(SET)
    slot_wanted = wanted.get(SLOT)
    main_stat_wanted = wanted.get(MAIN_STAT)
    starting_substats_wanted = wanted.get(STARTING_SUBSTATS)
    substats_wanted = wanted.get(SUBSTATS)
    rolls_wanted = wanted.get(ROLLS)
    roll_level_wanted = wanted.get(ROLL_LEVEL)

    artifact = {
        SET: 1 if source == 'Strongbox' else rand.choice([0, 1]),
        SLOT: rand.choice(slots),
        MAIN_STAT: '',
        STARTING_SUBSTATS: rand.choice(list(num_of_substats_probabilities[source].keys()),
                                       p=list(num_of_substats_probabilities[source].values())),
        SUBSTATS: [],
        ROLLS: [],
        ROLL_LEVEL: [],
        WANTED: 1
    }
    if (check_wanted(artifact.get(SET), set_wanted) or
        check_wanted(artifact.get(SLOT), slot_wanted) or
        check_wanted(artifact.get(STARTING_SUBSTATS), starting_substats_wanted)):
        artifact[WANTED] = 0
        return artifact

    artifact[MAIN_STAT] = select_main_stat(artifact[SLOT])
    if check_wanted(artifact.get(MAIN_STAT), main_stat_wanted):
        artifact[WANTED] = 0
        return artifact

    generate_substats(artifact)
    for _ in range(artifact[STARTING_SUBSTATS]+1):
        artifact.get(ROLLS).append(rand.choice([1, 2, 3, 4]))
        artifact.get(ROLL_LEVEL).append(roll_substat())
    return artifact

def domain_run() -> int:
    return rand.choice([1, 2], p=[0.935, 0.065])

def calculate_roll_values(artifact: dict) -> list:
    final_roll_values = [0] * 4
    flat_stats = {'HP', 'ATK', 'DEF', 'EM'}
    for roll, roll_level in zip(artifact[ROLLS], artifact[ROLL_LEVEL]):
        substat = artifact[SUBSTATS][roll - 1]
        max_value = substat_max_rolls[substat]
        final_roll_values[roll-1] += max_value * roll_level
    for index, substat in enumerate(artifact[SUBSTATS]):
        if substat in flat_stats:
            final_roll_values[index] = int(round(final_roll_values[index]))
        else:
            final_roll_values[index] = float(round(final_roll_values[index], 1))
    return final_roll_values

def print_result(result: dict):
    final_stats = calculate_roll_values(result)
    print(f"Set: {'Correct Set' if result[SET] == 1 else 'Wrong Set'}")
    print(f"Slot: {result[SLOT]}")
    print(f"Main Stat: {result[MAIN_STAT]}")
    print(f"Starting Substats: {result[STARTING_SUBSTATS]}")
    print(f"Substats:     {[str(x) for x in result[SUBSTATS]]}")
    print(f"No. of Rolls: {list(Counter(result[ROLLS]).values())}")
    print(f"Rolls:        {[int(x) for x in result[ROLLS]]}")
    print(f"Roll Levels:  {[float(x) for x in result[ROLL_LEVEL]]}")
    print(f"Stats:        {final_stats}")

def generate_and_print(source: str, wanted:dict = None):
    artifact_result = generate_artifact(source, wanted)
    print_result(artifact_result)

generate_and_print(DOMAIN, wanted={SET:1, STARTING_SUBSTATS:4})