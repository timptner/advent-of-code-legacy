from __future__ import annotations

import heapq
import logging

from enum import Enum

from utilities.backend import BasePuzzle
from utilities.models import Grid

logger = logging.getLogger(__name__)


class Direction(Enum):
    NORTH = (-1, 0)
    EAST = (0, 1)
    SOUTH = (1, 0)
    WEST = (0, -1)

    def left(self):
        switch = {
            self.NORTH: self.WEST,
            self.WEST: self.SOUTH,
            self.SOUTH: self.EAST,
            self.EAST: self.NORTH,
        }
        return switch[self]

    def right(self):
        switch = {
            self.NORTH: self.EAST,
            self.EAST: self.SOUTH,
            self.SOUTH: self.WEST,
            self.WEST: self.NORTH,
        }
        return switch[self]


OPPOSITE_DIRECTIONS = {
    Direction.NORTH: Direction.SOUTH,
    Direction.EAST: Direction.WEST,
    Direction.SOUTH: Direction.NORTH,
    Direction.WEST: Direction.EAST,
}


class Node:
    def __init__(self, row: int, column: int, direction: Direction) -> None:
        self.row = row
        self.column = column
        self.direction = direction

    def __repr__(self) -> str:
        return f"Node({self.row}, {self.column}, {self.direction})"

    def __eq__(self, other):
        if isinstance(other, Node):
            return all([
                self.row == other.row,
                self.column == other.column,
                self.direction == other.direction,
            ])
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


class State:
    def __init__(self, node: Node, previous: State = None, distance: int = 0) -> None:
        self.node = node
        self.previous = previous
        self.distance = distance

    def __repr__(self) -> str:
        if self.previous:
            previous_node = self.previous.node
        else:
            previous_node = None
        return f"State({self.node}, {previous_node}, {self.distance})"

    def __lt__(self, other) -> bool:
        return self.distance < other.distance

    def __eq__(self, other):
        if isinstance(other, State):
            return all([
                self.node == other.node,
                self.previous == other.previous,
                self.distance == other.distance,
            ])
        else:
            return False

    def __hash__(self):
        return hash(self.__repr__())


class Pathfinder(Grid):  # Dijkstra-Algorithm
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.active_states = []
        heapq.heapify(self.active_states)
        self.visited_states = set()

    def search(self, start_states: list[State], end_nodes: list[Node]) -> State:
        for state in start_states:
            heapq.heappush(self.active_states, state)

        distance = 0
        while self.active_states:
            # print(self.active_states)
            state = heapq.heappop(self.active_states)
            if distance < state.distance:
                print(f'{state.distance}({len(self.active_states)}, {len(self.visited_states)}).', end='')
                distance = state.distance
            if state in self.visited_states:
                continue
            self.get_next_states(state)
            self.visited_states.add(state)
            if state.node in end_nodes:
                return state

        raise Exception("No path found")

    def get_next_states(self, state: State) -> None:
        for direction in Direction:
            if direction == OPPOSITE_DIRECTIONS[state.node.direction]:
                continue
            if state.node.direction == direction:
                previous_state = state.previous
                last_directions = [state.node.direction]
                for n in range(2):
                    if previous_state is None:
                        break
                    previous_direction = previous_state.node.direction
                    if previous_direction != direction:
                        break
                    last_directions.append(previous_direction)
                    previous_state = previous_state.previous
                steps = 3 - len(last_directions)
            else:
                steps = 3
            distance = state.distance
            last_state = state
            for n in range(1, steps + 1):
                add_row, add_column = direction.value
                next_row = state.node.row + add_row * n
                next_column = state.node.column + add_column * n
                if not 0 <= next_row < self.size[0] or not 0 <= next_column < self.size[1]:
                    break
                node = Node(next_row, next_column, direction)
                distance += self.get_cost(next_row, next_column)
                next_state = State(node, last_state, distance)
                last_state = next_state
                heapq.heappush(self.active_states, next_state)

    def get_cost(self, row: int, column: int) -> int:
        if (row, column) in self.data.keys():
            cost = int(self.data[row, column])
        else:
            cost = 0
        return cost


class Puzzle(BasePuzzle):
    name = "Clumsy Crucible"
    year = 2023
    day = 17

    @property
    def test_data(self) -> dict:
        text = """
        2413432311323
        3215453535623
        3255245654254
        3446585845452
        4546657867536
        1438598798454
        4457876987766
        3637877979653
        4654967986887
        4564679986453
        1224686865563
        2546548887735
        4322674655533
        """
        return {
            'part1': (text, 102),
            'part2': (text, 0),
        }

    def part1(self, text: str) -> int:
        pathfinder = Pathfinder(text)
        start_states = [
            State(Node(0, 0, Direction.SOUTH)),
            State(Node(0, 0, Direction.EAST)),
        ]
        rows, columns = pathfinder.size
        end_nodes = [
            Node(rows - 1, columns - 1, Direction.EAST),
            Node(rows - 1, columns - 1, Direction.SOUTH),
        ]
        state = pathfinder.search(start_states, end_nodes)
        return state.distance

    def part2(self, text: str) -> int:
        pass
