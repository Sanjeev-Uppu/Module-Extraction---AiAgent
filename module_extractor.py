from crawler import crawl_docs
from content_parser import extract_content
from module_inferencer import infer_modules
from utils import validate_url

def run_extractor(urls):
    all_content = []

    for url in urls:
        if not validate_url(url):
            continue

        pages = crawl_docs(url)

        for html in pages.values():
            all_content.extend(extract_content(html))

    if not all_content:
        return []

    return infer_modules(all_content)
