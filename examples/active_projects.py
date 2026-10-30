"""A shortlist of active, licensed repositories for a query.

    python active_projects.py "pdf parser language:python" --months 6 --out shortlist.csv

Searches by stars and keeps the repositories that are not archived, not
forks, carry a license and were updated within the last --months months.
"""

import argparse
from datetime import datetime, timedelta, timezone
from typing import Optional

from quanticdata_github_repo_scraper import GitHubRepoScraper, write


def parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        moment = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return moment if moment.tzinfo else moment.replace(tzinfo=timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("query")
    parser.add_argument("--months", type=int, default=6, help="updated within this many months")
    parser.add_argument("--max", type=int, default=50, help="repositories to read (max 50)")
    parser.add_argument("--out", default="shortlist.csv")
    args = parser.parse_args()

    cutoff = datetime.now(timezone.utc) - timedelta(days=30 * args.months)
    github = GitHubRepoScraper()
    run = github.search(args.query, sort="stars", max_results=args.max)

    keep = []
    for r in run:
        updated = parse_time(r.get("updated_at"))
        if r.get("archived") or r.get("is_fork") or not r.get("license") or updated is None or updated < cutoff:
            continue
        keep.append(r)
        print(f"{r['repo']:45} {r.get('stars') or 0:>8} stars  {r['license']:14} updated {r['updated_at'][:10]}")

    write(keep, args.out)
    print(f"{len(keep)} of {len(run)} repositories kept, written to {args.out}")


if __name__ == "__main__":
    main()
