from rich import box
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel

stdout = Console()
stderr = Console(stderr=True, style='bold red')


def print_title(console: Console, title: str):
    panel = Panel.fit(title, box=box.ROUNDED, style='green')
    padding = Padding(panel, (1, 5))
    console.print(padding)
