"""Daily ranking of the most-starred repositories for a few queries.

    python ranking_watch.py "http client language:python" "static site generator" --top 20
    0 6 * * *  cd /path/to/here && python ranking_watch.py "http client language:python"

Appends one row per repository to ranking_history.csv: date, query, rank,
repository, stars, forks and open issues. Chart the file to see which
projects gain stars and places over time.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_github_repo_scraper import GitHubRepoScraper

FIELDS = ["date", "query", "rank", "repo", "stars", "forks", "open_issues", "updated_at"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("queries", nargs="+")
    parser.add_argument("--top", type=int, default=20, help="repositories per query (max 50)")
    parser.add_argument("--out", default="ranking_history.csv")
    args = parser.parse_args()

    github = GitHubRepoScraper()
    today = datetime.now(timezone.utc).date().isoformat()
    new_file = not os.path.exists(args.out)
    written = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for query in args.queries:
            for r in github.search(query, sort="stars", max_results=args.top):
                writer.writerow({"date": today, "query": query, **r})
                written += 1
    print(f"{written} rows appended to {args.out}")


if __name__ == "__main__":
    main()
