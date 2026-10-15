import os
import time
import subprocess
from rich.live import Live
from rich.table import Table
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console

# Config
BUS_DIR = "/storage/emulated/0/RootBase/modules/ccb_workbench_v1/.grimoire/bus"
LOG_DIR = "/data/data/com.termux/files/home/MikeySwarm/logs/archon"
CONSOLE = Console()

def get_bus_status():
    table = Table(title="Agent Bus Status")
    table.add_column("Agent", style="cyan")
    table.add_column("Last Task", style="green")
    
    files = sorted([f for f in os.listdir(BUS_DIR) if f.endswith('.json')], key=lambda f: os.path.getmtime(os.path.join(BUS_DIR, f)), reverse=True)
    for f in files[:5]:
        agent = f.split('_')[0]
        table.add_row(agent, "Active" if "completed" not in f else "Done")
    return table

def get_log_stream():
    logs = ""
    try:
        files = sorted([os.path.join(LOG_DIR, f) for f in os.listdir(LOG_DIR)], key=os.path.getmtime, reverse=True)
        with open(files[0], 'r') as f:
            logs = "".join(f.readlines()[-10:])
    except:
        logs = "No logs found."
    return Panel(logs, title="Archon Logs")

def generate_layout():
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body")
    )
    layout["body"].split_row(
        Layout(name="bus"),
        Layout(name="logs")
    )
    layout["header"].update(Panel("CCB Workbench Dashboard", style="bold white on blue"))
    layout["bus"].update(get_bus_status())
    layout["logs"].update(get_log_stream())
    return layout

with Live(generate_layout(), refresh_per_second=1) as live:
    while True:
        time.sleep(1)
        live.update(generate_layout())
