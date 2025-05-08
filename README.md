# CISA Advisories AI Agent

Scrapes Cybersecurity advisories listed at  https://www.cisa.gov/news-events/cybersecurity-advisories, parses all the advisories, using Firecrawl, prepares markup for each of the advisor so can be fed to a domain specific LLM 

## REST API

<details>
 <summary><code>GET</code> <code>/advisories</code> </summary>

##### Parameters

> | name        |  type     | data type      | description                 |
> |-----------  |-----------|----------------|-----------------------------|
> | `limit`     |  optional | int ($int64)   | Number of advisories        |
> | `max_depth` |  optional | int ($int64)   | Number of Pages deep        |

##### Responses

> | http code  | content-type               | response                                 |
> |------------|----------------------------|------------------------------------------|
> | `200`      | `text/plain`               | markdown string                          |
> | `400`      | `application/json`         | `{"code":"400","message":"Bad Request"}` |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" http://localhost:5000/advisories?limit=1&max_depth=1
> ```

</details>

<details>
 <summary><code>GET</code> <code>/search</code> </summary>

##### Parameters

> | name          |  type     | data type      | description                 |
> |---------------|-----------|----------------|-----------------------------|
> | `search_term` |  Required | str            | Search term                 |

##### Responses

> | http code  | content-type               | response                                 |
> |------------|----------------------------|------------------------------------------|
> | `200`      | `text/plain`               | markdown string                          |
> | `400`      | `application/json`         | `{"code":"400","message":"Bad Request"}` |

##### Example cURL

> ```javascript
>  curl -X GET -H "Content-Type: application/json" http://localhost:5000/search?search_term='improper access control'
> ```

</details>

## cli usage

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
[ransomware markup example](data/ransomware-markup.txt)