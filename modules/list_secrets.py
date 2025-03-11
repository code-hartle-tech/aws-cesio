from modules.base_plugin import BasePlugin
import boto3
from rich.console import Console
from rich.table import Table
import config
from main import clear_screen
from utils.loading import show_loading_message
from utils.aws_error_handler import handle_aws_errors  # ✅ Import global AWS error handler

console = Console()

class ListSecretsPlugin(BasePlugin):
    def __init__(self):
        super().__init__("List Secrets", "Security", "Lists AWS Secrets Manager secrets and IAM credentials.")

    @handle_aws_errors  # ✅ Apply global AWS error handling
    def run(self, region=None):
        if region is None:
            region = config.AWS_REGION

        clear_screen()
        show_loading_message()  # ✅ No more blank screen!

        session = boto3.Session(profile_name=config.AWS_PROFILE)
        secrets_client = session.client("secretsmanager", region_name=region)

        secrets = secrets_client.list_secrets()["SecretList"]

        if not secrets:
            console.print(f"[bold yellow]⚠ No secrets found in region {region}.[/bold yellow]")
        else:
            table = Table(title=f"[bold magenta]🔑 AWS Secrets ({region})[/bold magenta]".center(80), 
                          header_style="bold magenta", expand=True, show_lines=True)

            table.add_column("🔐 Secret Name", style="cyan", justify="left", no_wrap=True)
            table.add_column("📜 ARN", style="yellow", justify="left", no_wrap=True)
            table.add_column("📅 Created Date", style="blue", justify="left", no_wrap=True)
            table.add_column("⏳ Last Accessed", style="green", justify="left", no_wrap=True)

            for secret in secrets:
                table.add_row(secret["Name"], secret["ARN"], str(secret.get("CreatedDate", "N/A")), str(secret.get("LastAccessedDate", "N/A")))

            console.print(table)

        console.print("\n" + "═" * 80, style="dim")  # Fancy separator
        console.print("[bold cyan]🎉 Press [bright_yellow]ENTER[/bright_yellow] to return to the main menu![/bold cyan] 🎉\n")
        console.input()
