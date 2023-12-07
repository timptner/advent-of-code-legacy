from rich.align import Align
from rich.console import Console
from rich.padding import Padding
from rich.panel import Panel

console = Console(stderr=True)


def print_title(text: str):
    panel = Panel.fit(f"[bold magenta]{text}", title='[blue]Advent of Code', style='green')
    align = Align.center(panel)
    padding = Padding(align, 2)
    console.print(padding)
