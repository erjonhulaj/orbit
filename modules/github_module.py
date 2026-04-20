import requests
from config import Config

class GitHubModule:
    """Handles all communication with the GitHub API."""

    BASE_URL = "https://api.github.com"

    def __init__(self):
        # Auth header sent with every request
        self.headers = {
            "Authorization": f"token {Config.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = Config.GITHUB_USERNAME

    def get_profile(self) -> dict:
        """Fetch the GitHub profile of the user."""
        url = f"{self.BASE_URL}/users/{self.username}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch profile: {response.status_code} - {response.text}")
        
    def get_repositories(self) -> list:
        """Fetch the list of repositories for the user."""
        url = f"{self.BASE_URL}/users/{self.username}/repos"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch repositories: {response.status_code} - {response.text}")
            
    def get_top_languages(self, repos: list) -> dict:
        """Count language usage across all repositories, return sorted by frequency."""
        languages = {}
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        # Sort by count descending
        return dict(sorted(languages.items(), key=lambda item: item[1], reverse=True))
        
    def get_stats(self) -> dict:
        """Aggregate profile and repository stats into one clean dictionary."""
        profile = self.get_profile()
        repos = self.get_repositories()
        top_languages = self.get_top_languages(repos)

        return {
            "username": profile.get("login"),
            "name": profile.get("name"),
            "bio": profile.get("bio"),
            "followers": profile.get("followers"),
            "public_repos": profile.get("public_repos"),
            "total_stars": sum(repo.get("stargazers_count", 0) for repo in repos),
            "top_languages": top_languages,
            "repositories": [
                {
                    "name": repo.get("name"),
                    "stars": repo.get("stargazers_count"),
                    "language": repo.get("language"),
                    "description": repo.get("description"),
                    "url": repo.get("html_url")
                }
                for repo in repos
            ]
        }