from __future__ import annotations

import json
from typing import Any, Dict, List

from bs4 import BeautifulSoup


def parse_html(html: str) -> BeautifulSoup:
    return BeautifulSoup(html, "lxml")


def extract_meta(soup: BeautifulSoup) -> Dict[str, str | None]:
    def get_meta(name: str | None = None, prop: str | None = None) -> str | None:
        if name:
            tag = soup.find("meta", attrs={"name": name})
            if tag:
                return tag.get("content")
        if prop:
            tag = soup.find("meta", attrs={"property": prop})
            if tag:
                return tag.get("content")
        return None

    title_tag = soup.find("title")
    canonical_tag = soup.find("link", attrs={"rel": "canonical"})

    return {
        "title": title_tag.text.strip() if title_tag and title_tag.text else None,
        "meta_description": get_meta(name="description"),
        "og_title": get_meta(prop="og:title"),
        "og_description": get_meta(prop="og:description"),
        "og_image": get_meta(prop="og:image"),
        "canonical": canonical_tag.get("href") if canonical_tag else None,
    }


def extract_headings(soup: BeautifulSoup) -> Dict[str, List[str]]:
    h1 = [tag.get_text(" ", strip=True) for tag in soup.find_all("h1")]
    h2 = [tag.get_text(" ", strip=True) for tag in soup.find_all("h2")]
    return {"h1": h1, "h2": h2}


def extract_json_ld(soup: BeautifulSoup) -> List[Dict[str, Any]]:
    data: List[Dict[str, Any]] = []
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        if not script.string:
            continue
        try:
            payload = json.loads(script.string)
            if isinstance(payload, list):
                data.extend(item for item in payload if isinstance(item, dict))
            elif isinstance(payload, dict):
                data.append(payload)
        except json.JSONDecodeError:
            continue
    return data
