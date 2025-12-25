from bs4 import BeautifulSoup

def extract_content(html):
    """
    Extract meaningful documentation content from HTML
    """
    soup = BeautifulSoup(html, "html.parser")
    content_blocks = []

    for tag in soup.find_all(["h1", "h2", "h3", "p", "li", "td"]):
        text = tag.get_text(strip=True)
        if len(text) > 30:
            content_blocks.append(text)

    # Remove duplicates
    return list(set(content_blocks))
