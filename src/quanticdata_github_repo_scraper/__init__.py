"""GitHub Repository Search: GitHub repository search for Python and the command line: repositories for any query in GitHub search syntax, sorted by best match, stars or last update, with owner, description, language, stars, forks, topics, license and dates, as JSON or CSV. Free and open source; no GitHub token needed, sign in with your QuanticData account.

    from quanticdata_github_repo_scraper import GitHubRepoScraper

    scraper = GitHubRepoScraper()   # saved login (`github-repo-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.search(...)   # GitHub repository search results for a query
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["GitHubRepoScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class GitHubRepoScraper:
    """GitHub Repository Search on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="github-repo-scraper/0.1.0 (+https://github.com/quantumproxies/github-repo-scraper)", timeout=timeout)

    def search(
        self, query: str,
        *,
        sort: Optional[str] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """GitHub repository search for a query, in GitHub's search syntax: owner, name, description, language, stars, forks, open issues, topics, license, homepage and dates of each repository.

        Args:
            query: What to search, in GitHub's search syntax, e.g. "http client language:python" or "static site generator language:go stars:>500".
            sort: best_match (the default), stars or updated. One of: best_match, stars, updated.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many repositories to deliver at most (1–50). You pay only for delivered repositories.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 50 rows, one per repository: see ``types.GithubReposRow``.
        """
        payload = {
            "query": query,
            "sort": sort,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("github_repos", payload, wait=wait, timeout=timeout)
