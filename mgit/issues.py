import inflection
import requests
import os

from mgit import configs


class Issue:
    def __init__(self, id: str, summary: str, config=configs.Config()):
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

        >>> Issue(id='jir-123', summary='Update readme.md file')
        JIR-123: Update Readme.Md File
        """
        if self._id and self.title:
            return f"{self._id}: {self.title}"
        return self.title

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

        >>> Issue(summary='Update readme.md file')
        Update Readme.Md File
        """
        return inflection.titleize(self._summary)

    @property
    def url(self) -> str:
        """
        Return the URL for this issue

        >>> config = configs.Config({"issue_tracker_api": "http://example.com/"})
        >>> Issue(id=7, config=config).url
        http://example.com/7
        """
        return f"{self._config.issue_tracker_api}/{self._id}"


def from_branch(name: str, config=configs.Config()) -> Issue:
    """
    Create an Issue object from the name of a branch.

    :raises: ValueError if branch name does not contain an ID.

    >>> from_branch('jir-123-update-readme-file')
    JIR-123: Update Readme File
    >>> from_branch('123-update-readme-file')
    123: Update Readme File
    """
    parts = name.split("-")
    for index, part in enumerate(parts):
        if part.isdigit():
            id = "-".join(parts[: index + 1])
            summary = " ".join(parts[index + 1 :])
            break

    return Issue(id=id, summary=summary, config=config)


def from_tracker(issue_id: str, config=configs.Config()) -> Issue:
    """ Get Issue info by making an HTTP request. 
    
    :raises: requests.exceptions.HTTPError
    """
    res = requests.get(
        f"{config.issue_tracker_api.strip('/')}/{issue_id}",
        auth=_auth_values(config),
        headers={"content-type": "application/json"},
    )

    res.raise_for_status()
    summary = res.json().get("title", "")

    return Issue(issue_id, summary)


def _auth_values(config):
    if config.issue_tracker_is_github and os.getenv("MGIT_GITHUB_USERNAME"):
        return (
            os.getenv("MGIT_GITHUB_USERNAME"),
            os.getenv("MGIT_GITHUB_API_TOKEN"),
        )
    return None
