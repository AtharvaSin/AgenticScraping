"""Simple scraping utilities used by the executor."""

import httpx
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


def scrape_static(url, selectors, headers=None):
    r = httpx.get(url, headers=headers, timeout=15)
    soup = BeautifulSoup(r.text, "lxml")
    return [{k: soup.select_one(css).get_text(strip=True)} for k, css in selectors.items()]


def scrape_dynamic(url, selectors, ctx):
    with sync_playwright() as pw:
        browser = pw.firefox.launch()
        page = browser.new_page()
        page.goto(url, timeout=ctx.get("timeout", 10000))
        if "ready" in selectors:
            page.wait_for_selector(selectors["ready"])
        data = [{k: page.locator(css).inner_text()} for k, css in selectors.items() if k != "ready"]
        browser.close()
        return data

