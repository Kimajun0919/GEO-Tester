from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Set
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


@dataclass
class CrawledPage:
    url: str
    html: str


async def crawl_pages(url: str, multi_page: bool = False, max_pages: int = 3) -> List[CrawledPage]:
    pages: List[CrawledPage] = []
    visited: Set[str] = set()
    queue: List[str] = [url]
    domain = urlparse(url).netloc

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        try:
            while queue and len(pages) < max_pages:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)

                page = await context.new_page()
                try:
                    await page.goto(current, wait_until="domcontentloaded", timeout=30000)
                    html = await page.content()
                    pages.append(CrawledPage(url=current, html=html))

                    if multi_page and len(pages) == 1:
                        queue.extend(_extract_internal_links(current, html, domain, limit=max_pages * 2))
                finally:
                    await page.close()
        finally:
            await context.close()
            await browser.close()

    return pages


def _extract_internal_links(base_url: str, html: str, domain: str, limit: int = 10) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    links: List[str] = []
    seen: Set[str] = set()
    for anchor in soup.find_all("a", href=True):
        absolute = urljoin(base_url, anchor["href"])
        parsed = urlparse(absolute)
        if parsed.netloc != domain:
            continue
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/") or absolute
        if normalized in seen:
            continue
        seen.add(normalized)
        links.append(normalized)
        if len(links) >= limit:
            break
    return links


async def check_root_files(url: str) -> Dict[str, bool]:
    parsed = urlparse(url)
    root = f"{parsed.scheme}://{parsed.netloc}"
    targets = {
        "llms_txt": "/llms.txt",
        "ai_txt": "/ai.txt",
        "robots_txt": "/robots.txt",
        "sitemap_xml": "/sitemap.xml",
    }

    async with httpx.AsyncClient(follow_redirects=True, timeout=10) as client:
        results: Dict[str, bool] = {}
        for key, path in targets.items():
            try:
                response = await client.get(f"{root}{path}")
                results[key] = response.status_code == 200 and bool(response.text.strip())
            except httpx.HTTPError:
                results[key] = False
    return results
