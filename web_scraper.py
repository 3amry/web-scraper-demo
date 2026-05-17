#!/usr/bin/env python3
"""
web_scraper.py — General-purpose web scraper with Hacker News example

A clean, reusable scraping script that demonstrates:
  - HTML parsing with BeautifulSoup
  - Data extraction and structuring
  - CSV export
  - Error handling
  - Rate limiting awareness

Usage:
  python3 web_scraper.py              # scrapes Hacker News
  python3 web_scraper.py --help       # shows options

Requirements: requests, beautifulsoup4
"""

import csv
import sys
import time
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup


# ── Configuration ──────────────────────────────────────────────────────────

# Default target — a public, well-structured site for demo purposes
DEFAULT_URL = "https://news.ycombinator.com/"
REQUEST_TIMEOUT = 15  # seconds
REQUEST_DELAY = 1.0   # seconds between requests (be polite)
OUTPUT_FILE = "scraped_data.csv"


# ── Scraper ────────────────────────────────────────────────────────────────

def fetch_page(url: str) -> str | None:
    """Fetch a page and return its HTML, or None on failure."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }
    try:
        print(f"  Fetching: {url}")
        resp = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        return resp.text
    except requests.exceptions.Timeout:
        print(f"  ✗ Timeout: {url}")
    except requests.exceptions.HTTPError as e:
        print(f"  ✗ HTTP {e.response.status_code}: {url}")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Network error: {e}")
    return None


def parse_hacker_news(html: str) -> list[dict]:
    """
    Extract story data from Hacker News HTML.

    Returns a list of dicts with keys: title, url, score, author, comments.
    """
    soup = BeautifulSoup(html, "html.parser")
    stories = []

    # Hacker News uses a two-row structure per story:
    #   Row 1: title link + domain
    #   Row 2: score, author, comments link
    title_rows = soup.select("tr.athing")

    for title_row in title_rows:
        try:
            # ── Title and link ──
            title_span = title_row.select_one("td.title .titleline > a")
            if not title_span:
                continue
            title = title_span.get_text(strip=True)
            url = title_span.get("href", "")

            # ── Score, author, comments ──
            subtext_row = title_row.find_next_sibling("tr")
            subtext = subtext_row.select_one("td.subtext") if subtext_row else None

            score = 0
            author = ""
            comments = 0

            if subtext:
                score_span = subtext.select_one("span.score")
                if score_span:
                    score_text = score_span.get_text(strip=True)
                    score = int(score_text.split()[0]) if score_text.split() else 0

                author_link = subtext.select_one("a.hnuser")
                if author_link:
                    author = author_link.get_text(strip=True)

                # Last link in subtext row with "comment" text
                for link in subtext.find_all("a"):
                    text = link.get_text(strip=True)
                    if "comment" in text:
                        num = text.split()[0]
                        comments = int(num) if num.isdigit() else 0
                        break

            stories.append({
                "title": title,
                "url": url,
                "score": score,
                "author": author,
                "comments": comments,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            })

        except Exception as e:
            print(f"  ⚠ Skipped a row: {e}")
            continue

    return stories


def save_to_csv(data: list[dict], filename: str) -> str:
    """Write scraped data to CSV. Returns the absolute path."""
    if not data:
        print("  No data to save.")
        return ""

    fieldnames = data[0].keys()
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    return filename


# ── Main ───────────────────────────────────────────────────────────────────

def main():
    url = DEFAULT_URL
    if len(sys.argv) > 1 and sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return

    print(f"Web Scraper — {datetime.now(timezone.utc).isoformat()}")
    print(f"Target: {url}")
    print()

    # Step 1: Fetch
    html = fetch_page(url)
    if not html:
        sys.exit(1)

    # Step 2: Parse
    print("  Parsing...")
    time.sleep(REQUEST_DELAY)  # be polite
    results = parse_hacker_news(html)
    print(f"  Found {len(results)} items")

    # Step 3: Export
    path = save_to_csv(results, OUTPUT_FILE)
    if path:
        print(f"\n✓ Saved to: {path}")
        print(f"  Rows: {len(results)}")
    else:
        print("\n✗ Nothing saved")
        sys.exit(1)


if __name__ == "__main__":
    main()
