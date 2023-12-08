def first_part(data: str) -> int:
    instructions, nodes = data.split('\n\n')

    network = {}
    for line in nodes.splitlines():
        key, value = line.replace(' ', '').split('=')
        left, right = value[1:-1].split(',')
        network[key] = {'L': left, 'R': right}

    length = len(instructions)
    current_node = 'AAA'
    counter = 0
    while True:
        index = counter % length
        instruction = instructions[index]
        next_node = network[current_node][instruction]
        if length < 10:
            print(f"[{counter:06d}] {current_node} -> {next_node}")
        if next_node == 'ZZZ':
            break
        else:
            counter += 1
            current_node = next_node

    return counter + 1


def second_part(data: str) -> int:
    instructions, nodes = data.split('\n\n')

    network = {}
    for line in nodes.splitlines():
        key, value = line.replace(' ', '').split('=')
        left, right = value[1:-1].split(',')
        network[key] = {'L': left, 'R': right}

    current_nodes = [key for key in network.keys() if key.endswith('A')]
    amount = len(current_nodes)
    print(f"Doing {amount} path findings in parallel (still as sequential process...)")

    length = len(instructions)
    counter = 0
    while True:
        if counter % 10**6 == 0:
            print(counter)
        index = counter % length
        instruction = instructions[index]
        ends = []
        next_nodes = []
        for node in current_nodes:
            next_node = network[node][instruction]
            next_nodes.append(next_node)
            if next_node.endswith('Z'):
                ends.append(True)
            else:
                ends.append(False)
        if length < 10:
            print(f"[{counter:06d}] {current_nodes} -> {next_nodes}")
        if all(ends):
            break
        else:
            counter += 1
            current_nodes = next_nodes

    return counter + 1
