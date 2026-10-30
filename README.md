# GitHub Repository Search

[![ci](https://github.com/quantumproxies/github-repo-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/github-repo-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

GitHub repository search from Python or the command line: send a query and get the matching repositories as rows, with owner, name, description, primary language, stars, forks, open issues, topics, license, homepage and creation and update dates, as JSON or CSV. Queries take GitHub's own search syntax (language:python, stars:>100) and sort by best match, stars or last update. The code is free and open source (MIT). It runs on the QuanticData Data API, so there is no GitHub token to create: sign in to QuanticData once and run a query.

```bash
pip install git+https://github.com/quantumproxies/github-repo-scraper
github-repo-scraper login
github-repo-scraper search "http client language:python" --sort stars -o repos.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `github-repo-scraper search` | query in GitHub search syntax | Repo, description, language, stars, forks, topics, license, dates, 19 fields per row ([fields and price](https://quanticdata.io/collectors/github-repository-search-api/?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper)) | up to 50 |

Narrow the query with GitHub's qualifiers, such as `language:python` or `stars:>500`, and order it with `--sort stars` or `--sort updated`. Every row says whether the repository is `archived` or a fork (`is_fork`), and whether its owner is a user or an organization (`owner_type`).

## Sample output

A real row from `github-repo-scraper search "http client language:python" --sort stars --max-results 3` (2026-10-23):

```json
{
  "url": "https://github.com/psf/requests",
  "name": "requests",
  "rank": 1,
  "repo": "psf/requests",
  "forks": 12916,
  "owner": "psf",
  "stars": 54613,
  "topics": [
    "client",
    "cookies",
    "forhumans",
    "http",
    "humans",
    "python",
    "python-requests",
    "requests"
  ],
  "is_fork": false,
  "license": "Apache-2.0",
  "archived": false,
  "homepage": "https://requests.readthedocs.io/en/latest/",
  "language": "Python",
  "created_at": "2011-02-13T18:38:17Z",
  "owner_type": "Organization",
  "updated_at": "2026-09-28T16:55:48Z",
  "description": "A simple, yet elegant, HTTP library.",
  "open_issues": 244,
  "default_branch": "main"
}
```

## Python

```python
from quanticdata_github_repo_scraper import GitHubRepoScraper

github = GitHubRepoScraper()  # saved login, or QUANTICDATA_API_KEY

repos = github.search("http client language:python", sort="stars", max_results=20)
for r in repos:
    print(r["repo"], r["stars"], r["forks"], r["license"], r["updated_at"])
repos.to_csv("python_http_clients.csv")

recent = github.search("static site generator language:go stars:>500", sort="updated", max_results=10)
print([r["repo"] for r in recent if not r["archived"]])
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Top repositories per language**: Run one topic across several languages and get the most-starred repositories of each in one CSV, with the language the row was searched for. See [`examples/top_by_language.py`](examples/top_by_language.py).
- **Active, licensed projects**: Search a topic and keep only the repositories that are not archived, not forks, carry a license and were updated in the last months: a shortlist of projects you can depend on. See [`examples/active_projects.py`](examples/active_projects.py).
- **Ranking watch**: Append the top results of a few queries, with stars and forks, to a CSV every day and see which projects gain ground. See [`examples/ranking_watch.py`](examples/ranking_watch.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `github-repo-scraper run <id> -o out.csv` collects it later.

### `github-repo-scraper search`

GitHub repository search for a query, in GitHub's search syntax: owner, name, description, language, stars, forks, open issues, topics, license, homepage and dates of each repository.

```
github-repo-scraper search QUERY [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `QUERY` | string |  | What to search, in GitHub's search syntax, e.g. "http client language:python" or "static site generator language:go stars:&gt;500". |
| `--sort` | best_match / stars / updated | `best_match` | best_match (the default), stars or updated. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `20` | How many repositories to deliver at most (1–50). You pay only for delivered repositories. |

## Output fields

<details><summary><code>github-repo-scraper search</code>: 19 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position. |
| `repo` | string | owner/name. |
| `owner` | string or null | Owner login. |
| `name` | string or null | Repository name. |
| `description` | string or null | Repo description. |
| `language` | string or null | Primary language. |
| `stars` | integer or null | Star count. |
| `topics` | string[] | Repo topics. |
| `archived` | boolean | Archived flag. |
| `updated_at` | string or null | Last update (ISO 8601). |
| `url` | string | Repository URL. |
| `forks` | integer or null | Fork count. |
| `open_issues` | integer or null | Open issues and pull requests. |
| `license` | string or null | License (SPDX id). |
| `homepage` | string or null | Project homepage. |
| `created_at` | string or null | Repository creation time (ISO 8601). |
| `default_branch` | string or null | Default branch. |
| `is_fork` | boolean or null | Whether the repository is a fork. |
| `owner_type` | string or null | User or Organization. |

</details>

## Sign-in and API keys

- `github-repo-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `github-repo-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `github-repo-scraper login --api-key`.
- `github-repo-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/github_repos/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"query": "http client language:python", "sort": "stars", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this GitHub repo scraper free?**

The code is free and MIT-licensed. Searches run on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on the collector page. Failed runs are never billed.

**Do I need a GitHub token or proxies?**

No. There is no personal access token to create and no proxy to configure: you send a query and get the repositories back; the requests run on QuanticData's side.

**Does it support GitHub's search qualifiers?**

Yes. The query is GitHub search syntax, so qualifiers such as language:python and stars:>100 narrow the results; --sort orders them by best_match, stars or updated.

**How many repositories can one search return?**

Up to 50 repositories per run, 20 by default: raise it with --max-results and you pay only for what is delivered.

**Can I export to CSV?**

Add -o repos.csv (or .json, .jsonl). Topics are joined with '; ', so the file opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/ranking_watch.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Package Registry API](https://github.com/quantumproxies/package-registry-api): Package registry API for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=github-repo-scraper).
