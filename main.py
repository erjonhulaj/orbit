from config import Config
from modules.github_module import GitHubModule

# Validate configuration before starting the app
Config.validate()

# Instantiate the GitHub module
github = GitHubModule()
stats = github.get_stats()

# Print raw output for now, will replace with a nice UI later
print(stats)