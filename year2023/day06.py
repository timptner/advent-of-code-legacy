import numpy as np


def calculate_strategies(times: np.ndarray, distances: np.ndarray) -> int:
    races = np.stack([times, distances]).transpose()
    strategies = []
    for time, distance in races:
        hold_time = time - np.arange(time + 1)
        speed = hold_time
        race_distance = speed * (time - hold_time)
        total = np.count_nonzero(np.where(race_distance > distance, race_distance, 0))
        strategies.append(total)
    return np.array(strategies).prod()


def first_part(data: str) -> int:
    lines = data.splitlines()
    times = np.array([int(number) for number in lines[0].removeprefix('Time:').split()])
    distances = np.array([int(number) for number in lines[1].removeprefix('Distance:').split()])
    strategies = calculate_strategies(times, distances)
    return strategies


def second_part(data: str) -> int:
    lines = data.splitlines()
    times = np.array([int(lines[0].removeprefix('Time:').replace(' ', ''))])
    distances = np.array([int(lines[1].removeprefix('Distance:').replace(' ', ''))])
    strategies = calculate_strategies(times, distances)
    return strategies
