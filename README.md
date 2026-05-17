# Python Web Scraper — Portfolio Demo

A clean, reusable web scraper that extracts data from public websites and outputs it as CSV.

Built with: **Python, Requests, BeautifulSoup4**

## Example: Hacker News Front Page

Running the script against `news.ycombinator.com` extracts 30 stories with title, URL, score, author, and comment count:

| Title | Score | Comments |
|---|---|---|
| Zerostack – A Unix-inspired coding agent written in pure Rust | 492 | 269 |
| Mozilla to UK regulators: VPNs are essential privacy and security tools | 467 | 209 |
| We've made the world too complicated | 392 | 373 |
| SANA-WM, a 2.6B open-source world model for 1-minute 720p video | 378 | 144 |
| I don't think AI will make your processes go faster | 276 | 221 |
| Moving away from Tailwind, and learning to structure my CSS | 620 | 349 |
| Security researcher says Microsoft built a Bitlocker backdoor | 270 | 125 |
| A nicer voltmeter clock | 264 | 32 |
| Every AI Subscription Is a Ticking Time Bomb for Enterprise | 232 | 188 |
| Apple Silicon costs more than OpenRouter | 188 | 157 |

Full output: [sample-output.csv](sample-output.csv) (30 rows, 6 columns)

## What This Demonstrates

- **HTML parsing** with BeautifulSoup — handles complex DOM structures
- **Data extraction** — picks out specific elements (titles, scores, metadata)
- **CSV export** — clean, ready-to-use output files
- **Error handling** — gracefully skips malformed rows, handles timeouts and HTTP errors
- **Rate limiting** — polite delays between requests, proper User-Agent headers

## How to Use

```bash
pip3 install requests beautifulsoup4
python3 web_scraper.py
```

To scrape a different site, modify `DEFAULT_URL` in the script and implement a parser function for that site's HTML structure.

## Adaptable For

- Product data from e-commerce sites
- Job listings from boards
- Directory/contact information
- News/article aggregation
- Price monitoring
- Any public website with structured data

---

*Built by [3amry](https://github.com/3amry) — Civil Engineer & Python Automation*
