from abc import abstractmethod
from enum import Enum

from utilities.backend import BasePuzzle


class Pulse(Enum):
    LOW = 0
    HIGH = 1


class Message:
    def __init__(self, sender: str, recipient: str, pulse: Pulse) -> None:
        self.sender = sender
        self.recipient = recipient
        self.pulse = pulse

    def __repr__(self) -> str:
        return f"Message({self.sender}, {self.recipient}, {self.pulse})"

    def __str__(self) -> str:
        return str(self.pulse)


class Network:
    def __init__(self):
        self.modules = {}
        self.messages = []
        self.stats = {
            Pulse.LOW: 0,
            Pulse.HIGH: 0,
        }

    def add_module(self, module) -> None:
        self.modules[module.name] = module

    def start(self) -> None:
        while self.messages:
            message = self.messages.pop(0)
            self.stats[message.pulse] += 1
            # print(message.sender, f'-{message.pulse}->', message.recipient)
            module = self.modules[message.recipient]
            module.receive(message)


class BaseModule:
    def __init__(self, network: Network, name: str, connections: list) -> None:
        self.network = network
        self.name = name
        self.connections = connections

    def __repr__(self) -> str:
        return f"Module({self.name})"

    def __str__(self) -> str:
        return self.name

    @abstractmethod
    def receive(self, message: Message) -> None:
        raise NotImplementedError


class State(Enum):
    OFF = 0
    ON = 1


class FlipFlopModule(BaseModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.state = State.OFF

    def receive(self, message: Message) -> None:
        if message.pulse == Pulse.HIGH:
            return

        if self.state == State.OFF:
            self.state = State.ON
            pulse = Pulse.HIGH
        else:
            self.state = State.OFF
            pulse = Pulse.LOW

        for name in self.connections:
            new_message = Message(self.name, name, pulse)
            self.network.messages.append(new_message)


class ConjunctionModule(BaseModule):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.memory = {}

    def init(self, names: list[str]) -> None:
        for name in names:
            self.memory[name] = Pulse.LOW

    def receive(self, message: Message) -> None:
        self.memory[message.sender] = message.pulse

        if all([pulse.value for pulse in self.memory.values()]):
            pulse = Pulse.LOW
        else:
            pulse = Pulse.HIGH

        for name in self.connections:
            new_message = Message(self.name, name, pulse)
            self.network.messages.append(new_message)


class BroadcastModule(BaseModule):
    def receive(self, message: Message) -> None:
        for name in self.connections:
            new_message = Message(self.name, name, message.pulse)
            self.network.messages.append(new_message)


class ButtonModule(BaseModule):
    def receive(self, message: Message) -> None:
        pass

    def push(self) -> None:
        for name in self.connections:
            message = Message(self.name, name, Pulse.LOW)
            self.network.messages.append(message)
            self.network.start()


class TesterModule(BaseModule):
    def receive(self, message: Message) -> None:
        if message.recipient == 'rx' and message.pulse == Pulse.LOW:
            raise ValueError


class Puzzle(BasePuzzle):
    year = 2023
    day = 20
    name = "Pulse Propagation"

    @property
    def test_data(self) -> dict:
        text = """
        broadcaster -> a
        %a -> inv, con
        &inv -> b
        %b -> con
        &con -> output
        """
        return {
            'part1': (text, 11687500),
            'part2': (text, None),
        }

    def part1(self, text: str) -> int:
        network = Network()

        button = ButtonModule(network, 'button', ['broadcaster'])
        network.add_module(button)
        network.add_module(TesterModule(network, 'output', []))
        network.add_module(TesterModule(network, 'rx', []))

        for line in text.splitlines():
            name, connections = line.split(' -> ')
            connections = connections.replace(' ', '').split(',')
            if name.startswith('%'):
                module = FlipFlopModule(network, name[1:], connections)
            elif name.startswith('&'):
                module = ConjunctionModule(network, name[1:], connections)
            else:
                module = BroadcastModule(network, name, connections)
            network.add_module(module)

        senders = {}
        for name, module in network.modules.items():
            for module_name in module.connections:
                if module_name in senders.keys():
                    senders[module_name].append(name)
                else:
                    senders[module_name] = [name]

        for key, value in senders.items():
            module = network.modules[key]
            if isinstance(module, ConjunctionModule):
                module.init(value)

        for n in range(1000):
            button.push()

        high, low = network.stats.values()
        return high * low

    def part2(self, text: str) -> int:
        pass
