import time

import requests

from src.workspace_context import CANDIDATE_REPOSITORY_FILE, get_repository_file_path, write_json_file, HEADERS


def get_issue_pr_number(repo_owner: str, repo_name: str, type: str) -> int:
    try:
        issue_pr_url = f"https://api.github.com/search/issues?q=repo:{repo_owner}/{repo_name}+is:{type}"
        response = requests.get(issue_pr_url, headers=HEADERS)
        if response.status_code == 200:
            if "total_count" in response.json():
                number_of_issues_prs = response.json()["total_count"]
            else:
                return 0
        else:
            return 0
    except requests.exceptions.RequestException as e:
        return 0
    # Limiting API requests to 30 requests per minute
    time.sleep(2)
    return number_of_issues_prs


def fetch_most_popular_java_repositories_with_issues(
    number_of_repositories, issue_minimum, pr_minimum
):
    params = {
        "q": f"language:java",
        "sort": "stars",
        "order": "desc",
        "page": "1",
        "per_page": str(number_of_repositories),
        "since": "2022-01-01T00:00:00Z",
        "before": "2021-01-01T00:00:00Z",
    }
    response = requests.get(
        "https://api.github.com/search/repositories", headers=HEADERS, params=params
    )
    if response.status_code == 200:
        data = response.json()
        repositories = data["items"]
        candidate_repositories = {"candidate_repositories": []}
        for repo in repositories:
            repo_name = repo["name"]
            print(repo_name)
            repo_owner = repo["owner"]["login"]
            issue_number = get_issue_pr_number(repo_owner, repo_name, "issue")
            pr_number = get_issue_pr_number(repo_owner, repo_name, "pr")

            if issue_number > issue_minimum and pr_number > pr_minimum:
                repository_url = f"https://github.com/{repo_owner}/{repo_name}"
                candidate_repositories["candidate_repositories"].append(repository_url)
                if len(candidate_repositories) == number_of_repositories:
                    break
            else:
                continue
        return candidate_repositories
    else:
        return None

def fetch_repository_task():
    number_of_repositories = 10
    issue_minimum = 500
    pr_minimum = 500
    candidate_repositories = fetch_most_popular_java_repositories_with_issues(
        number_of_repositories, issue_minimum, pr_minimum
    )
    repository_file_path = get_repository_file_path(CANDIDATE_REPOSITORY_FILE)
    write_json_file(repository_file_path, candidate_repositories)


if __name__ == "__main__":
    fetch_repository_task()