"""Minimal GitHub repository search API call — one typed row per repository.

Docs & schema: https://quanticdata.io/collectors/github-repository-search-api/
"""
import json
import os

import requests

API = "https://api.quanticdata.io/v1/scraper/collectors/github_repos/run"
KEY = os.environ["QD_API_KEY"]  # https://quanticdata.io/

payload = {
        "query": "web scraper",
        "sort": "stars",
        "max_results": 20
    }

r = requests.post(
    API,
    headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
    json=payload,
    timeout=180,
)
r.raise_for_status()
data = r.json()["payload"]

for row in data["results"]:
    print(row.get("repo"), row.get("owner"), row.get("name"))
print(f"{len(data['results'])} repositorys, cost ${data['cost']}")
