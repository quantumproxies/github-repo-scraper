"""Most-starred repositories of one topic in several languages, in one CSV.

    python top_by_language.py "web framework" --languages python go rust typescript --top 10

Runs "<topic> language:<language>" sorted by stars for each language and
writes top_by_language.csv, each row with the language it was searched for.
"""

import argparse

from quanticdata_github_repo_scraper import GitHubRepoScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("topic")
    parser.add_argument("--languages", nargs="+", required=True)
    parser.add_argument("--top", type=int, default=10, help="repositories per language (max 50)")
    parser.add_argument("--out", default="top_by_language.csv")
    args = parser.parse_args()

    github = GitHubRepoScraper()
    rows = []
    for language in args.languages:
        run = github.search(f"{args.topic} language:{language}", sort="stars", max_results=args.top)
        leader = f"{run.rows[0]['repo']} ({run.rows[0]['stars']} stars)" if len(run) else "none"
        print(f"{language}: {len(run)} repositories, first {leader}")
        rows.extend({"searched_language": language, **r} for r in run)

    write(rows, args.out)
    print(f"{len(rows)} rows written to {args.out}")


if __name__ == "__main__":
    main()
