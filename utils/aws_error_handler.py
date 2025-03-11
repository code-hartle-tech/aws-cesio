import sys
from rich.console import Console
import botocore.exceptions

console = Console()

def handle_aws_errors(func):
    """Decorator to catch and handle AWS authentication-related errors globally."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] in ["ExpiredToken", "RequestExpired"]:
                console.print("\n[bold red]❌ AWS session has expired! Please refresh your credentials.[/bold red]")
                console.print("Run the following command to re-authenticate:")
                console.print("\n[bold yellow]aws sso login --profile cesio-user[/bold yellow] (if using SSO)")
                console.print("[bold yellow]aws configure --profile cesio-user[/bold yellow] (if using IAM keys)\n")
                sys.exit(1)
            else:
                console.print(f"\n[bold red]❌ AWS Error:[/bold red] {e.response['Error']['Message']}")
                sys.exit(1)
        except botocore.exceptions.NoCredentialsError:
            console.print("\n[bold red]❌ No AWS credentials found![/bold red] Please configure your AWS credentials.")
            console.print("Run the following command to set up AWS credentials:")
            console.print("\n[bold yellow]aws configure --profile cesio-user[/bold yellow]\n")
            sys.exit(1)
        except botocore.exceptions.EndpointConnectionError:
            console.print("\n[bold red]❌ Unable to connect to AWS![/bold red] Check your internet connection and region settings.")
            sys.exit(1)

    return wrapper
