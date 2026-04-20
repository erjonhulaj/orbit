from config import Config
from modules.github_module import GitHubModule
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

# Validate configuration before starting the app
Config.validate()

# Instantiate the GitHub module
github = GitHubModule()
stats = github.get_stats()

# Display profile summary in a panel
profile_text = (
    f"[bold]Username:[/bold] {stats['username']}\n"
    f"[bold]Followers:[/bold] {stats['followers']}\n"
    f"[bold]Public Repositories:[/bold] {stats['public_repos']}\n"
    f"[bold]Total Stars:[/bold] {stats['total_stars']}"
)
console.print(Panel(profile_text, title="GitHub Profile Summary", border_style="cyan"))

#Display top languages in a table
lang_table = Table(title="Top Languages Used", border_style="cyan")
lang_table.add_column("Language", style="bold white")
lang_table.add_column("Repositories", style="cyan", justify="right")

for lang, count in stats['top_languages'].items():
    lang_table.add_row(lang, str(count))
console.print(lang_table)

# Display repository details in a table
repo_table = Table(title="Repositories", border_style="cyan")
repo_table.add_column("Name", style="bold white")
repo_table.add_column("Language", style="cyan")
repo_table.add_column("Stars", style="yellow", justify="right")
repo_table.add_column("Description", style="dim")

for repo in stats['repositories']:
    repo_table.add_row(
        repo['name'],
        repo['language'] or "N/A",
        str(repo['stars']),
        repo['description'] or "No description"
    )
console.print(repo_table)