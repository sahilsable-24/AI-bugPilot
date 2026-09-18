from playwright.sync_api import Page, sync_playwright
from urllib.parse import urlparse, urljoin

def is_same_domain(link:str, base_url:str) -> bool:
    link_netloc = urlparse(link).netloc
    base_netloc = urlparse(link).netloc

    if link_netloc == "" or link_netloc == base_netloc:
        return True
    


def inspect_page(page:Page) -> dict:
    title = page.title()
    links = [a.get_attribute("href") for a in page.locator("a").all()]
    internal_links = [i for i in links if is_same_domain(i,page.url)]
    external_links = [i for i in links if not is_same_domain(i,page.url)]
    return {
        "title": title,
        "internal_links": internal_links,
        "external_links": external_links
    }

def crawl(start_url:str, max_page:int =10):
    visited: set[str] = set()
    queue: list[str] = [start_url]

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        while queue and len(visited) < max_page:

            url = queue.pop(0)

            if url in visited:
                continue

            page.goto(url)
            result = inspect_page(page)
            visited.add(url)

            print(f"[{len(visited)}] {result["title"]} - {url}")

            for link in result["internal_links"]:
                absolute_link = urljoin(url,link)
                if absolute_link not in visited:
                    queue.append(absolute_link)

        browser.close()

crawl("https://books.toscrape.com/")