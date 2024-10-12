#!/usr/bin/env python
from rich.console import Console
from rich.table import Table
import math

def print_logtable():
    console = Console()

    table = Table()

    table.add_column("n", justify="right")
    table.add_column("log_10(n)", justify="right")
    
    for n in range(1, 10):
        table.add_row(f"{n/10}", f"{math.log10(n/10)*100:.1f}%")

    for n in range(1, 11):
        table.add_row(f"{n}", f"{math.log10(n)*100:.1f}%")


    constants = { "ℇ": math.e, "π": math.pi }

    for repr, n in constants.items():
        table.add_row(repr, f"{math.log10(n)*100:.1f}%")


    console.print(table)
