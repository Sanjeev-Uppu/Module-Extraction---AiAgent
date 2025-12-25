import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def crawl_docs(base_url, max_pages=30):
    """
    Recursively crawl documentation pages starting from base_url
    """
    visited = set()
    queue = [base_url]
    pages = {}

    base_domain = urlparse(base_url).netloc

    while queue and len(visited) < max_pages:
        current_url = queue.pop(0)

        if current_url in visited:
            continue

        try:
            response = requests.get(current_url, timeout=10)
            if response.status_code != 200:
                continue

            visited.add(current_url)
            pages[current_url] = response.text

            soup = BeautifulSoup(response.text, "html.parser")

            for link in soup.find_all("a", href=True):
                href = link["href"]
                full_url = urljoin(current_url, href)

                parsed = urlparse(full_url)

                if (
                    parsed.netloc == base_domain
                    and full_url not in visited
                    and any(x in full_url.lower() for x in ["help", "docs", "support"])
                ):
                    queue.append(full_url)

        except Exception:
            # Handles broken links, timeouts, redirects safely
            continue

    return pages
