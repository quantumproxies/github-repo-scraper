# GitHub repository search API — examples

Repository search — name, description, language, stars, topics. No token, no API quota.

**Live page, full schema & pricing → [quanticdata.io/collectors/github-repository-search-api/](https://quanticdata.io/collectors/github-repository-search-api/)**

Searches GitHub repositories and delivers one row per repo: owner/name, description, primary language, star count, topics, archived flag and last-update time. Read from the server-rendered search page (10 per page), so it needs no GitHub token and is not subject to the unauthenticated API's 10-requests-per-minute limit. Supports GitHub's full search syntax (stars:>1000, language:python…).

## Quick start (curl)

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/github_repos/run \
  -H "Authorization: Bearer $QD_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "web scraper", "sort": "stars", "max_results": 20}'
```

## Python

See [`example.py`](example.py):

```bash
export QD_API_KEY=qd_live_...   # https://quanticdata.io/
python3 example.py
```

## Inputs

- `query` (string, required) — Search query — GitHub syntax works ("web scraper language:python stars:>100").
- `sort` (string) — best_match (default), stars, or updated.
- `country` (string) — ISO 3166-1 alpha-2 code — proxy exit geo and Google locale (gl). Omit for the default pool.
- `max_results` (integer) — How many repositories to deliver at most (1–50). You pay only for delivered repositories.

## Output — one row per repository

| field | type | description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `repo` | string | owner/name. |
| `owner` | string | Owner login. |
| `name` | string | Repository name. |
| `description` | string | Repo description. |
| `language` | string | Primary language. |
| `stars` | integer | Star count. |
| `topics` | string[] | Repo topics. |
| `archived` | boolean | Archived flag. |
| `updated_at` | string | Last update (ISO 8601). |
| `url` | string | Repository URL. |

## Pricing

**$0.0005 per delivered repository** ($0.5 per 1,000). A run that delivers nothing costs nothing, and failed rows are never billed. The $2/month free allowance covers roughly 4,000 repositorys — no card required.

## Links

- This collector: https://quanticdata.io/collectors/github-repository-search-api/
- All collectors: https://quanticdata.io/collectors/
- Docs: https://quanticdata.io/docs/
