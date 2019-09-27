import inflection
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

    def __str__(self):
        """
        Return ID and title case summary of the issue.

        >>> issue = Issue(id='jir-123', summary='Update readme.md file')
        >>> print(issue)
        JIR-123: Update Readme.Md File
        """
        return f"{self._id}: {self.title()}"

    @classmethod
    def from_branch(cls, name: str, config=Config()):
        """
        Create an Issue object from the name of a branch.

        >>> Issue.from_branch('jir-123-update-readme-file')
        JIR-123: Update Readme File
        >>> Issue.from_branch('123-update-readme-file')
        123: Update Readme File
        """
        parts = name.split("-")
        for index, part in enumerate(parts):
            if part.isdigit():
                id = "-".join(parts[: index + 1])
                summary = " ".join(parts[index + 1 :])
                break
        return Issue(id=id, summary=" ".join(summary), config=config)

    def branch_name(self) -> str:
        """
        Get the branch name from ID and title.

        >>> issue = Issue(id='jir-123', summary='Update readme.md file')
        >>> issue.branch_name()
        jir-123-update-readme-file
        """
        return inflection.parameterize(f"{self._id} {self._summary}")

    def title(self) -> str:
        """
        Titleized the summary of the issue.

        >>> issue = Issue(summary='Update readme.md file')
        >>> print(issue.title())
        Update Readme.Md File
        """
        return inflection.titleize(self._summary)

    def url(self) -> str:
        """ Return the URL for this issue. """
        return f"{self._config.issue_tracker_api}/{self._id}"
