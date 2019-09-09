import inflection


class Issue:
    def __init__(self, id: str, summary: str):
        """
        :param id: Issue ID.
        :param summary: Issue summary.
        """
        self._id = id.upper()
        self._summary = summary

    def __str__(self):
        """
        Return ID and title case summary of the issue.

        >>> issue = Issue(id='jir-123', summary='Update readme.md file')
        >>> print(issue)
        JIR-123: Update Readme.Md File
        """
        return f"{self._id}: {self.title()}"

    @classmethod
    def from_branch(cls, name: str):
        """
        Create an Issue object from the name of a branch.

        >>> Issue.from_branch('jir-123-update-readme-file')
        JIR-123: Update Readme File
        """
        project, ticket_id, *summary = name.split("-")
        return Issue(id=f"{project}-{ticket_id}", summary=" ".join(summary))

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
        # TODO: Change this to accommodate other issue trackers (GitHub, Trello, etc)
        link = os.getenv("JIRA_SITE_URL", default=Issue.DEFAULT_SITE_URL).strip("/")
        return f"{link}/browse/{self._id}"
