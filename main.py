import os
import signal
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from utils.plugin_loader import load_plugins
from config import get_aws_region, get_aws_profiles  # ✅ Import missing functions
import random  # For funny loading messages

console = Console()

def clear_screen():
    """Clears the terminal screen properly."""
    os.system("cls" if os.name == "nt" else "clear")  # Clears screen

def signal_handler(sig, frame):
    """Gracefully handle CTRL+C exit."""
    console.print("\n[bold red]👋 Exiting AWS Toolkit. See you next time![/bold red]")
    exit(0)

# Capture CTRL+C
signal.signal(signal.SIGINT, signal_handler)

def display_menu(title, options):
    """Display a menu with selectable options and return the user's choice."""
    clear_screen()  # Clears screen before showing menu

    # ✅ Add "Exit" as an option
    options["E"] = "🚪 Exit the program"

    table = Table(title=f"[bold magenta]{title.center(50)}[/bold magenta]", 
                  header_style="bold magenta", expand=True, show_lines=True)
    
    # ✅ Updated column name to "🎲 Number"
    table.add_column("🎲 Number", style="yellow", justify="center", min_width=6, max_width=6, no_wrap=True)
    table.add_column("📌 Description", style="cyan", justify="left", no_wrap=False)

    for key, desc in options.items():
        table.add_row(f"{key}", f"[bold]{desc}[/bold]")  # ✅ Removed 🔹

    console.print(table)

    console.print("\n" + "═" * 60, style="dim")  # Fancy separator
    choice = Prompt.ask(f"\nSelect an option (Press [bright_yellow]ENTER[/bright_yellow] for default)", default="1").strip().lower()

    # ✅ Allow exit with "e"
    if choice == "e":
        console.print("\n[bold red]👋 Exiting AWS Toolkit. See you next time![/bold red]")
        exit(0)

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(options) - 1:  # -1 to exclude "E"
        console.print("[bold red]❌ Invalid choice! Using the default option.[/bold red]")
        choice = "1"

    return choice




def select_aws_profile():
    """Let the user select an AWS profile, defaulting to the first one if ENTER is pressed."""
    available_profiles = get_aws_profiles()

    if not available_profiles:
        console.print("[bold red]⚠ No AWS profiles found! Please configure AWS CLI using `aws configure`.⚠[/bold red]")
        exit(1)

    console.print("\n[bold cyan]📌 Select an AWS Profile:[/bold cyan]")
    table = Table(title="🌍 AWS Profiles".center(60), header_style="bold magenta", expand=True, show_lines=True)
    
    table.add_column("🎲 Option", style="yellow", justify="center", min_width=4, max_width=4, no_wrap=True)
    table.add_column("🆔 Profile Name", style="cyan", justify="left")

    for idx, profile in enumerate(available_profiles, start=1):
        table.add_row(f"{idx}", profile)

    console.print(table)

    console.print("\n" + "═" * 60, style="dim")  # Fancy separator
    choice = Prompt.ask("\nSelect a profile (Press ENTER to use default)", default="1")

    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(available_profiles):
        console.print("[bold red]❌ Invalid choice! Using the default profile.[/bold red]")
        choice = "1"

    selected_profile = available_profiles[int(choice) - 1]

    console.print(f"\n[bold green]✅ Selected AWS Profile: {selected_profile}[/bold green]")
    return selected_profile


def main():
    """Main menu loop."""
    import config  # Import inside function to avoid circular import issues

    config.AWS_PROFILE = select_aws_profile()  # Select profile
    config.AWS_REGION = get_aws_region(config.AWS_PROFILE)  # ✅ Ensure region is set

    console.print(f"\n[bold cyan]🌍 Using AWS Region: {config.AWS_REGION}[/bold cyan]")

    while True:
        clear_screen()
        console.print("\n[bold green]🚀 AWS Toolkit - Plugin System[/bold green]\n")

        plugins = load_plugins()
        if not plugins:
            console.print("[bold red]No plugins found![/bold red]")
            return

        categories = {
            "Compute": ["List Instances"],
            "Security": ["List Secrets"],
        }

        while True:
            clear_screen()
            console.print("\n[bold cyan]📌 Select a Category:[/bold cyan]")
            category_choice = display_menu("AWS Plugin Categories", {cat: f"Plugins for {cat}" for cat in categories.keys()})

            if category_choice == "back":
                break

            selected_category = list(categories.keys())[int(category_choice) - 1]
            available_plugins = {p: plugins[p].description for p in categories[selected_category] if p in plugins}

            clear_screen()
            plugin_choice = display_menu(f"🔍 {selected_category} Plugins", available_plugins)
            if plugin_choice == "back":
                continue

            selected_plugin = list(available_plugins.keys())[int(plugin_choice) - 1]

            clear_screen()
            console.print(f"\n[bold cyan]Running {selected_plugin} in region {config.AWS_REGION}...[/bold cyan]\n")

            plugins[selected_plugin].run(config.AWS_REGION)

if __name__ == "__main__":
    main()
