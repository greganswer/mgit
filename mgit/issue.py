import inflection
import requests
import os

from .config import Config


class Issue:
    def __init__(self, id: str, summary: str, config=Config()):
        """
        :param id: Issue ID.
        :param summary: Issue summary.
        """
        self._id = id.upper()
        self._summary = summary
        self._config = config

    def __str__(self) -> str:
        """
        Return ID and title case summary of the issue.

        >>> issue = Issue(id='jir-123', summary='Update readme.md file')
        >>> print(issue)
        JIR-123: Update Readme.Md File
        """
        return f"{self._id}: {self.title}"

    @property
    def id(self) -> str:
        return self._id

    @property
    def branch_name(self) -> str:
        """
        Get the branch name from ID and title.

        >>> issue = Issue(id='jir-123', summary='Update readme.md file')
        >>> issue.branch_name()
        jir-123-update-readme-file
        """
        return inflection.parameterize(f"{self._id} {self._summary}")

    @property
    def title(self) -> str:
        """
        Titleized the summary of the issue.

        >>> issue = Issue(summary='Update readme.md file')
        >>> print(issue.title)
        Update Readme.Md File
        """
        return inflection.titleize(self._summary)

    @property
    def url(self) -> str:
        """
        Return the URL for this issue

        >>> config = Config({"issue_tracker_api": "http://example.com/"})
        >>> issue = Issue(id=7, config=config)
        >>> print(issue.url)
        http://example.com/7
        """
        return f"{self._config.issue_tracker_api}/{self._id}"


def get_from_tracker(issue_id: str, config=Config()) -> Issue:
    """ Get Issue info by making an HTTP request. 
    
    :raises: equests.exceptions.HTTPError
    """
    url = f"{config.issue_tracker_api.strip('/')}/{issue_id}"
    auth = _get_auth_values(config)
    headers = {"content-type": "application/json"}
    res = requests.get(url, auth=auth, headers=headers)
    res.raise_for_status()

    summary = ""
    if config.issue_tracker_is_github:
        summary = res.json()["title"]
    # TODO: replace with `res.json().get("title", "")`

    return Issue(issue_id, summary)


def get_from_branch(name: str, config=Config()) -> Issue:
    """
    Create an Issue object from the name of a branch.

    >>> get_from_branch('jir-123-update-readme-file')
    JIR-123: Update Readme File
    >>> get_from_branch('123-update-readme-file')
    123: Update Readme File
    """
    parts = name.split("-")
    for index, part in enumerate(parts):
        if part.isdigit():
            id = "-".join(parts[: index + 1])
            summary = " ".join(parts[index + 1 :])
            break

    return Issue(id=id, summary=summary, config=config)


def _get_auth_values(config):
    if config.issue_tracker_is_github and os.getenv("MGIT_GITHUB_USERNAME"):
        return (
            os.getenv("MGIT_GITHUB_USERNAME"),
            os.getenv("MGIT_GITHUB_API_TOKEN"),
        )
    return None
