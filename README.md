# cisa-advisor

Scrapes Cybersecurity advisories listed at  https://www.cisa.gov/news-events/cybersecurity-advisories, parses all the advisories, prepares markup for each of the advisor so can be fed to an LLM 

## Usage

```                               
python services/cisa.py [-h] [--output-dir OUTPUT_DIR] [--max-pages MAX_PAGES] [--max-advisories MAX_ADVISORIES] [--verbose]

Scrape CISA cybersecurity advisories

options:
  -h, --help            show this help message and exit
  --output-dir OUTPUT_DIR
                        Directory to save the output files (default: target)
  --max-pages MAX_PAGES
                        Maximum number of pages to scrape (default: 5)
  --max-advisories MAX_ADVISORIES
                        Maximum number of advisories to scrape (default: 50)
  --verbose             Enable verbose output for debugging
```
### Sample markup
[icsa-25-091-01](data/Rockwell-advisory.json)