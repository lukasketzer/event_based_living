
import requests
from bs4 import BeautifulSoup
import string
from typing import Iterable, Tuple


def clean_name(name):
    """Clean the name by removing unwanted characters."""
    for char in string.punctuation:
        name = name.replace(char, "_")
    return name.strip().lower()


def crawl(
    inital_sites: set[str],
    skip: set[str] = set(),
    max_depth: int = -1,
    num_results: int = -1,
    verbose: bool = False,
) -> Iterable[Tuple[str, str]]:
    """
    Recursively crawls a set of initial websites, following links up to a specified depth,
    and saves the text content of each visited page to a file.

    Args:
        inital_sites (set[str]): Initial URLs to start crawling from.
        skip (set[str], optional): Substrings; URLs containing any are skipped.
        max_depth (int, optional): Maximum crawl depth. -1 means unlimited.

    Side Effects:
        - Creates 'scraper/results' directory if missing.
        - Removes existing '.txt' files in 'scraper/results'.
        - Writes text content of each crawled page to a file.

    Notes:
        - Only 'http' and '/' links are followed.
        - Skipped URLs are not visited.
        - Prints status code or error for each site.
    """

    sites_depths = [inital_sites]
    visited = set()
    # Fetch each site and print the status code
    for depth in range(max_depth):
        urls = sites_depths[depth]

        # add next depth level
        sites_depths.append(set())

        for url in urls:
            if len(visited) >= num_results > 0:
                return

            for s in skip:
                if s in url:
                    continue

            if url in visited:
                continue

            try:
                response = requests.get(url)
                visited.add(url)

                soup = BeautifulSoup(response.content, "html.parser")
                anchors = soup.find_all("a")
                for anchor in anchors:
                    sub_url = anchor.get("href")  # type: ignore
                    if sub_url is None:
                        continue

                    sub_url = str(sub_url).strip()

                    if sub_url.startswith("http") and sub_url not in visited:
                        sites_depths[-1].add(sub_url)
                    if sub_url.startswith("/"):
                        sub_url = url + sub_url[1:]

                text = soup.get_text(separator=" ", strip=True)
                yield url, text

            except requests.RequestException as _:
                continue


if __name__ == "__main__":

    # Create results directory if it doesn't exist
    import os
    from pathlib import Path
    current_file_parent = Path(__file__).resolve().parent

    (current_file_parent / "results").mkdir(parents=True, exist_ok=True)

    # Read the sites from the file
    with open(current_file_parent / "sites.txt", "r") as file:
        initial_urls = file.readlines()

    initial_urls = set([site.strip() for site in initial_urls if site.strip()])
    initial_urls = set([site for site in initial_urls if not site.startswith("#")])

    skip = {"youtube.com", "youtu.be", "facebook.com", "instagram.com", "x.com"}

    for url, text in crawl(initial_urls, skip=skip, max_depth=5, num_results=10):
        print(url)
