import click
import subprocess
import sys
import requests
from .git import *
from .issue import Issue


class App:
    def __init__(self, log_file, verbose: bool):
        """
        :param log_file: The file where log output is sent.
        :param verbose: Determine if additional info should be logged.
        """
        self._log_file = log_file
        self._verbose = verbose

    def branch(self, issue_id: str, base_branch: str):
        """ Create a branch using issue ID and title. """
        if not base_branch:
            base_branch = default_base_branch()
        new_branch = self.get_issue(issue_id).branch_name()
        self.echo(
            f"This will create a branch off {self.green(base_branch)} named {self.green(new_branch)}."
        )
        self.confirm_or_abort()
        self.execute_or_exit(f"git checkout {base_branch}")
        self.execute_or_exit(f"git pull")
        self.execute_or_exit(f"git checkout -b {new_branch}")

    def commit(self, message: str):
        """ Create a commit and push to GitHub. """
        if not message:
            try:
                message = Issue.from_branch(current_branch()).title()
            except ValueError:
                self.log(
                    (
                        f"The {current_branch()} branch does not contain an issue ID and title.\n"
                        "Please use a different branch or provide the --message option to provide a custom message for this commit."
                    )
                )
                sys.exit(1)
        self.echo(
            (
                f"This will do the following:\n"
                f"    - Add all uncommitted files\n"
                f"    - Add all uncommitted files\n"
                f'    - Create a commit with the message "{self.green(message)}"\n'
                f"    - Push the changes to origin\n"
            )
        )
        self.confirm_or_abort()
        self.safe_execute("git add .")
        self.safe_execute(f"git commit -m {message}")
        self.execute_first_success(
            "git push", f"git push --set-upstream origin {current_branch()}"
        )

    def open(self):
        """ Open an issue in the Google Chrome browser. """

    def pull_request(self, base_branch: str):
        """ Create a GitHub Pull Request for the specified branch. """

    # Helpers

    def execute(self, command: str):
        """ Execute a command on the terminal and log errors to log file. """
        if self._verbose:
            self.log(f"Executing command -> {command}")
        return subprocess.check_output(command.split(), stderr=self._log_file)

    def safe_execute(self, command: str):
        """ Execute a command on the terminal and ignore errors. """
        try:
            self.execute(command)
        except subprocess.CalledProcessError:
            pass

    def execute_or_exit(self, command: str):
        """ Execute a command on the terminal and exit if error occurs. """
        try:
            self.execute(command)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)

    def execute_first_success(self, *commands):
        """ Execute commands until the first one succeeds. """
        for command in commands:
            try:
                return self.execute(command)
            except subprocess.CalledProcessError:
                pass

    # Issue Helpers

    def get_issue(self, issue_id: str) -> Issue:
        """ Get Issue info by making an HTTP request. """
        # TODO: Use config value to determine what API to request issue info from.
        url = "http://www.mocky.io/v2/5d78f3f13000003c3f31f89e"
        res = requests.get(url, headers={"content-type": "application/json"})
        title = res.json()["fields"]["summary"]
        return Issue(issue_id, title)

    # Click Helpers

    def echo(self, message: str):
        """ Echo a message to the terminal. """
        click.echo(message)

    def confirm_or_abort(self):
        """ Abort unless the user confirms that they wish to continue. """
        click.confirm("Do you wish to continue?", abort=True)

    def confirm(self, message: str, abort=False):
        """ Get user confirmation. """
        click.confirm(message, abort=abort)

    def log(self, message: str):
        """ Log message to the log_file. """
        click.echo(message, file=self._log_file)

    # Colors

    def blue(self, message, bold=False):
        return click.style(message, fg="blue", bold=bold)

    def green(self, message, bold=False):
        return click.style(message, fg="green", bold=bold)

    def red(self, message, bold=False):
        return click.style(message, fg="red", bold=bold)

    def yellow(self, message, bold=False):
        return click.style(message, fg="yellow", bold=bold)