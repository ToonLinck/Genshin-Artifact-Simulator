import const as const
import numpy as np
from collections import Counter

rand = np.random.default_rng()
DOMAIN = const.ARTIFACT_SOURCE.DOMAIN
STRONGBOX = const.ARTIFACT_SOURCE.STRONGBOX

SET = 'Set'
SLOT = 'Slot'
MAIN_STAT = 'Main Stat'
STARTING_SUBSTATS = 'Starting Substats'
SUBSTATS = 'Substats'
ROLLS = 'Rolls'
ROLL_LEVEL = 'Roll Level'
WANTED = 'Wanted'






class substat:
    

    def __init__(self,stat:const.SUBMAIN_STATS_NAMES,):
        self.stat = stat


class Artifact:

    def __init__(self,set:str , slot:str , main_stat, sub_stats):
        self.set = set
        self.slot = slot
        self.main_stat = main_stat
        self.sub_stats = sub_stats

    pass

def generate_substats(artifact: dict):
    main_stat = artifact.get(MAIN_STAT)
    substats = artifact.get(SUBSTATS)
    rolls = artifact.get(ROLLS)
    roll_level = artifact.get(ROLL_LEVEL)

    for i in range(4):
        remaining_substats = [key for key in const.SUBSTAT_WEIGHTS if key not in substats and key != main_stat]
        substat_key_sum = sum(const.SUBSTAT_WEIGHTS[key] for key in remaining_substats)
        substat_probabilities = [const.SUBSTAT_WEIGHTS[key] / substat_key_sum for key in remaining_substats]
        generated_substat = rand.choice(remaining_substats, p=substat_probabilities)
        substats.append(generated_substat)
        rolls.append(i+1)
        roll_level.append(roll_substat())

def roll_substat() -> float:
    return rand.choice([0.7, 0.8, 0.9, 1])

def select_main_stat(slot):
    probabilities = const.MAIN_STAT_PROBABILITY[slot]
    return rand.choice(list(probabilities), p=list(probabilities.values()))

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
        SET: 1 if source == const.ARTIFACT_SOURCE.STRONGBOX else rand.choice([1,2]),
        SLOT: rand.choice(const.SLOTS),
        MAIN_STAT: '',
        STARTING_SUBSTATS: rand.choice(list(const.NUM_OF_SUBSTATS_PROBABILITIES[source].keys()),
                                       p=list(const.NUM_OF_SUBSTATS_PROBABILITIES[source].values())),
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
        max_value = const.SUBSTAT_MAX_ROLLS[substat]
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