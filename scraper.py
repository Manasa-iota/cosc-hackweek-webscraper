import os
import csv
import requests
from bs4 import BeautifulSoup
from typing import List, Tuple


class GitHubTrendingScraper:
    """
    Scrapes the top trending repositories from GitHub and saves them to a CSV file.

    Attributes:
        url (str): The GitHub trending page URL.
        output_dir (str): Directory where the output CSV will be saved.
        output_file (str): Full path to the output CSV file.
        max_repos (int): Number of top repositories to scrape.
    """

    def __init__(self, url: str = "https://github.com/trending", output_dir: str = "data", max_repos: int = 5):
        """
        Initializes the GitHubTrendingScraper with target URL and output settings.

        Args:
            url (str): The URL to scrape. Defaults to GitHub Trending.
            output_dir (str): The directory to save the CSV file. Defaults to 'data'.
            max_repos (int): The number of repositories to extract. Defaults to 5.
        """
        self.url: str = url
        self.output_dir: str = output_dir
        self.output_file: str = os.path.join(self.output_dir, "trending_repos.csv")
        self.max_repos: int = max_repos

    def fetch_html(self) -> str:
        """
        Sends a GET request to the GitHub Trending page and retrieves the HTML content.

        Returns:
            str: The HTML content of the trending page.

        Raises:
            SystemExit: If the request fails due to network issues or bad response.
        """
        try:
            with requests.get(self.url, timeout=10) as response:
                response.raise_for_status()
                return response.text
        except requests.RequestException as error:
            raise SystemExit(f"Failed to fetch data: {error}")

    def parse_repositories(self, html: str) -> List[Tuple[str, str]]:
        """
        Parses the HTML to extract repository names and links.

        Args:
            html (str): HTML content of the GitHub trending page.

        Returns:
            list[tuple[str, str]]: A list of tuples containing repository name and link.
        """
        soup = BeautifulSoup(html, "html.parser")
        anchors = soup.select("article.Box-row h2.h3 a")[:self.max_repos]

        repositories: List[Tuple[str, str]] = []
        for anchor in anchors:
            name: str = anchor.get_text(strip=True).replace(" ", "")
            link: str = f"https://github.com{anchor['href']}"
            repositories.append((name, link))

        return repositories

    def export_to_csv(self, repos: List[Tuple[str, str]]) -> None:
        """
        Saves the repository data to a CSV file.

        Args:
            repos (list[tuple[str, str]]): A list of (name, link) tuples.
        """
        os.makedirs(self.output_dir, exist_ok=True)

        with open(self.output_file, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Repository Name", "Repository Link"])
            writer.writerows(repos)

    def run(self) -> None:
        """
        Executes the scraping process:
        - Fetches HTML
        - Parses repository data
        - Writes to CSV
        """
        html = self.fetch_html()
        repos = self.parse_repositories(html)
        self.export_to_csv(repos)
        print(f"Scraped top {self.max_repos} repositories to: {self.output_file}")