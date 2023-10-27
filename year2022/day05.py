#! /usr/bin/env python3

import re

from utilities.storage import read_data


def get_containers(line: str) -> list:
    count = int((len(line) + 1) / 4)
    containers = []
    for number in range(count):
        index = number * 4 + 1
        container = line[index]
        containers.append(container)
    return containers


def parse_containers(container_set: str) -> list:
    container_set = list(reversed(container_set.splitlines()))
    container_set.pop(0)
    stacks = []
    for level in container_set:
        containers = get_containers(level)
        stacks.append(containers)
    stacks = list(zip(*stacks))
    stacks = [list(''.join(stack).rstrip()) for stack in stacks]
    return stacks


def parse_instructions(instruction_set: str) -> list:
    instructions = []
    for line in instruction_set.splitlines():
        match = re.match(r'^move\s(\d+)\sfrom\s(\d)\sto\s(\d)$', line)
        if match is None:
            raise ValueError(f"Invalid line. [line='{line}']")
        instruction = [int(number) for number in match.groups()]
        instruction[1] += -1
        instruction[2] += -1
        instructions.append(instruction)
    return instructions


def pop_multiple(stack: list, amount: int,
                 move_multiple: bool = False) -> tuple:
    containers = []
    for index in range(amount):
        container = stack.pop()
        if move_multiple:
            containers.insert(0, container)
        else:
            containers.append(container)
    return containers, stack


def validate_version(version: int) -> None:
    versions = [9000, 9001]
    if version not in versions:
        raise ValueError(f"Invalid CrateMover Version. [choices={versions}]")


def execute_instructions(stacks: list, instructions: list,
                         version: int = 9000) -> list:
    validate_version(version)
    for amount, origin, target in instructions:
        containers, stacks[origin] = pop_multiple(
            stacks[origin],
            amount,
            True if version == 9001 else False,
        )
        for container in containers:
            stacks[target].append(container)
    return stacks


def reorder_crates(version: int = 9000) -> str:
    validate_version(version)

    data = read_data(2022, 5)
    container_set, instruction_set = data.split('\n\n')

    stacks = parse_containers(container_set)
    instructions = parse_instructions(instruction_set)

    stacks = execute_instructions(stacks, instructions, version)
    top_crates = []
    for stack in stacks:
        container = stack[-1]
        top_crates.append(container)

    return ''.join(top_crates)


def main() -> None:
    part1 = reorder_crates(version=9000)
    print(f"Part 1: {part1}")

    part2 = reorder_crates(version=9001)
    print(f"Part 2: {part2}")


if __name__ == '__main__':
    main()
