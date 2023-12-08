import math


def parse_data(data: str) -> tuple[list[int], dict[str, tuple[str, str]]]:
    instructions, nodes = data.split('\n\n')

    converter = {
        'L': 0,
        'R': 1,
    }
    instructions = [converter[instruction] for instruction in instructions]

    network = {}
    for line in nodes.splitlines():
        key, value = line.replace(' ', '').split('=')
        left, right = value[1:-1].split(',')
        network[key] = (left, right)

    return instructions, network


def get_steps(instructions: list[int], network: dict[str, tuple[str, str]],
              start_node: str, end_node: list[str]) -> int:
    length = len(instructions)
    current_node = start_node
    counter = 0
    while True:
        index = counter % length
        instruction = instructions[index]
        next_node = network[current_node][instruction]
        if next_node in end_node:
            break
        else:
            counter += 1
            current_node = next_node
    return counter + 1


def first_part(data: str) -> int:
    instructions, network = parse_data(data)
    steps = get_steps(instructions, network, 'AAA', ['ZZZ'])
    return steps


def second_part(data: str) -> int:
    instructions, network = parse_data(data)

    start_nodes = []
    end_nodes = []
    for key in network.keys():
        if key.endswith('A'):
            start_nodes.append(key)
        if key.endswith('Z'):
            end_nodes.append(key)

    list_of_steps = []
    for start_node in start_nodes:
        steps = get_steps(instructions, network, start_node, end_nodes)
        list_of_steps.append(steps)

    total_steps = math.lcm(*list_of_steps)
    return total_steps
