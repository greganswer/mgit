import click  # https://click.palletsprojects.com/en/7.x/

# TODO: Extract to JSON or YAML file.
MESSAGES = {
    "create_branch_warning": "This will create a branch off {base_branch} named {new_branch}.",
    "issue_tracker_api_prompt": "Enter the API URL for your issue tracker",
    "hub_cli_missing": "This script relies on GitHub's 'hub' command line tool.\nVisit https://github.com/github/hub to install it",
}


class Translator:
    def __getattr__(self, name):
        def method_missing(**kwargs):
            """
            Get the value in MESSAGES based on the method name.

            >>> t = Translator()
            >>> t.issue_tracker_api_prompt()
            Enter the API URL for your issue tracker
            """
            return MESSAGES[name].format(**kwargs)

        return method_missing

    def init_issue_tracker_api(self):
        return f"""In order to retrieve the issue info we need the issue tracker API. Examples:
    - GitHub: https://api.github.com/repos/:owner/:repo/issues"""

    def issue_tracker_api_prompt(self):
        return "Enter the API URL for your issue tracker"

    def hub_cli_missing(self):
        return f"""This script relies on GitHub's 'hub' command line tool.
Visit https://github.com/github/hub to install it"""

    def invalid_git_directory(self):
        return "Please make sure you're in the parent directory for this repository."

    def create_branch_warning(self, base_branch, new_branch):
        # return MESSAGES["create_branch_warning"].format(self.green(base_branch), self.green(new_branch))
        return f"This will create a branch off {self.green(base_branch)} named {self.green(new_branch)}."

    def branch_has_no_issue_id(self, current_branch):
        # TODO: Add MESSAGES constant dictionary with
        # return MESSAGES["branch_has_no_issue_id"].format(current_branch)
        return f"""The {current_branch} branch does not contain an issue ID and title.
Please use a different branch or provide the --message option to provide a custom message for this commit."""

    def closes_issue_id(self, id):
        return f"\n\nCloses #{id}"

    def commit_warning(self, message):
        # TODO:
        # return MESSAGES["commit_warning"].format(self.green(message))

        return f"""This will do the following:
    - Add all uncommitted files
    - Create a commit with the message "{self.green(message)}"
    - Push the changes to origin"""

    def pull_request_warning(self, message, base_branch, title):
        return f"""This will do the following:
    - Add all uncommitted files
    - Create a commit with the message "{self.green(message)}"
    - Push the changes to origin
    - Create a pull request to the {self.green(base_branch)} branch with the title "{self.green(title)}"
    - Open the pull request in your web browser"""

    def update_base_branch_confirmation(self, base_branch):
        return f"Would you like to update the {self.green(base_branch)} branch first and rebase your commits?"

    def pull_request_body(self, title, issue_tracker, id, url):
        return f"""{title}

# [{issue_tracker} ticket {id}]({url})

# Screenshots

# Sample API Requests

# QA Steps


# Checklist
- [] Added tests
- [] Check for typos
- [] Updated CHANGELOG.md
- [] Updated internal/external documentation"""

    # Colors

    def blue(self, message):
        return click.style(message, fg="blue")

    def green(self, message):
        return click.style(message, fg="green")

    def red(self, message):
        return click.style(message, fg="red")

    def yellow(self, message):
        return click.style(message, fg="yellow")
