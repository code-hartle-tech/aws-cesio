from modules.base_plugin import BasePlugin
import boto3
from rich.console import Console
from rich.table import Table
import config
from main import clear_screen
from utils.loading import show_loading_message  # ✅ Import loading message

console = Console()

class ListInstancesPlugin(BasePlugin):
    def __init__(self):
        super().__init__("List Instances", "Compute", "Displays all EC2 instances with their names.")

    def run(self, region=None):
        if region is None:
            region = config.AWS_REGION

        clear_screen()
        show_loading_message()  # ✅ No more blank screen!

        session = boto3.Session(profile_name=config.AWS_PROFILE)
        ec2_client = session.client("ec2", region_name=region)

        instances = ec2_client.describe_instances()["Reservations"]

        if not instances:
            console.print("[bold yellow]⚠ No instances found in this region.[/bold yellow]")
        else:
            table = Table(title=f"[bold cyan]🚀 EC2 Instances ({region})[/bold cyan]", 
                          header_style="bold cyan", expand=True, show_lines=True)

            # ✅ Fix: Adjusted column widths for perfect alignment
            table.add_column("📺 Name", style="magenta", justify="left", min_width=22, max_width=25, no_wrap=True)
            table.add_column("🔑 ID", style="yellow", justify="left", min_width=20, max_width=22, no_wrap=True)
            table.add_column("🚦 State", style="green", justify="center", min_width=12, max_width=14, no_wrap=True)
            table.add_column("🍕 Type", style="blue", justify="left", min_width=18, max_width=20, no_wrap=True)
            table.add_column("🌍 Public IP", style="magenta", justify="center", min_width=17, max_width=18, no_wrap=True)
            table.add_column("🏠 Private IP", style="magenta", justify="center", min_width=17, max_width=18, no_wrap=True)

            for reservation in instances:
                for instance in reservation["Instances"]:
                    name_tag = "N/A"
                    if "Tags" in instance:
                        for tag in instance["Tags"]:
                            if tag["Key"] == "Name":
                                name_tag = tag["Value"]
                                break

                    state_icon = "🟢 Running" if instance["State"]["Name"] == "running" else "🔴 Stopped"

                    table.add_row(
                        f"{name_tag}",  # ✅ Added spacing & a wrench icon for uniqueness
                        instance["InstanceId"],
                        f"[bold]{state_icon}[/bold]",
                        instance["InstanceType"],
                        instance.get("PublicIpAddress", "[dim]N/A[/dim]"),
                        instance.get("PrivateIpAddress", "[dim]N/A[/dim]"),
                    )

            console.print(table)

        console.print("\n" + "═" * 80, style="dim")  # Fancy separator
        console.print("[bold cyan]🎉 Press [bright_yellow]ENTER[/bright_yellow] to return to the main menu![/bold cyan] 🎉\n")
        console.input()
