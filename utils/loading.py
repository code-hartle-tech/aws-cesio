import random
from rich.console import Console

console = Console()

def show_loading_message():
    """Displays a random funny loading message."""
    messages = [
        "🛒 We're fetching the required information... Need eggs or milk on the way back?",
        "🚀 Hold on! We're zooming through the AWS universe to get your data!",
        "🐱 Cats are cute, but we promise this is a productive use of your time.",
        "☕ Coffee break? AWS is cooking up your request!",
        "🎩 Running cloud magic spells... just a moment!",
        "🕵️‍♂️ Investigating AWS secrets... almost there!",
        "🌎 Fetching instances... and checking if Earth is still spinning.",
    ]
    message = random.choice(messages)
    console.print(f"\n[bold cyan]{message}[/bold cyan]\n")
