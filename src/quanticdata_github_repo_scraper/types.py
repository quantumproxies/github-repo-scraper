"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class GithubReposRow(TypedDict, total=False):
    """One row of `github-repo-scraper search` (github_repos v1.1.1)."""

    rank: int
    """1-based position."""
    repo: str
    """owner/name."""
    owner: Optional[str]
    """Owner login."""
    name: Optional[str]
    """Repository name."""
    description: Optional[str]
    """Repo description."""
    language: Optional[str]
    """Primary language."""
    stars: Optional[int]
    """Star count."""
    topics: List[str]
    """Repo topics."""
    archived: bool
    """Archived flag."""
    updated_at: Optional[str]
    """Last update (ISO 8601)."""
    url: str
    """Repository URL."""
    forks: Optional[int]
    """Fork count."""
    open_issues: Optional[int]
    """Open issues and pull requests."""
    license: Optional[str]
    """License (SPDX id)."""
    homepage: Optional[str]
    """Project homepage."""
    created_at: Optional[str]
    """Repository creation time (ISO 8601)."""
    default_branch: Optional[str]
    """Default branch."""
    is_fork: Optional[bool]
    """Whether the repository is a fork."""
    owner_type: Optional[str]
    """User or Organization."""
