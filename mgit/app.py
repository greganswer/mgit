import click
import subprocess
import sys
import requests
import json
import os
from .git import *
from .config import Config
from .issue import Issue


class App:
    def __init__(self, log_file, verbose: bool, config=Config()):
        """
        Initialize the app by validating the environment.

        :param log_file: The file where log output is sent.
        :param verbose: Determine if additional info should be logged.
        """
        self._log_file = log_file
        self._verbose = verbose
        self._config = config

        # Validate there is a .git folder
        if not os.path.isdir(".git"):
            self.log(
                "Please make sure you're in the parent directory for this repository."
            )
            sys.exit(1)

        # Prompt the user for config values if the project mgit.json file does not exist.
        if not os.path.isfile(Config.filename):
            self._config_init()

    def branch(self, issue_id: str, base_branch: str):
        """ Create a branch using issue ID and title. """
        if not base_branch:
            base_branch = default_base_branch()
        new_branch = self.get_issue_or_abort(issue_id).branch_name()

        self.echo(
            f"This will create a branch off {self.green(base_branch)} named {self.green(new_branch)}."
        )
        self.confirm_or_abort()
        self.execute_or_abort(f"git checkout {base_branch}")
        self.execute_or_abort(f"git pull")
        self.execute_or_abort(f"git checkout -b {new_branch}")

    def commit(self, message: str, issue_id: str):
        """ Create a commit and push to GitHub. """
        issue = None
        if not message:
            try:
                if issue_id:
                    issue = self.get_issue_or_abort(issue_id)
                else:
                    issue = Issue.from_branch(current_branch())
            except ValueError:
                self.log(
                    (
                        # TODO: Extract to private method
                        f"The {current_branch()} branch does not contain an issue ID and title.\n"
                        "Please use a different branch or provide the --message option to provide a custom message for this commit."
                    )
                )
                sys.exit(1)
            message = issue.title()
        if issue and self._config.issue_tracker_is_github():
            message += f"\n\nCloses #{issue.id}"
        self.echo(
            (
                # TODO: Extract to private method
                f"This will do the following:\n"
                f"    - Add all uncommitted files\n"
                f'    - Create a commit with the message "{self.green(message)}"\n'
                f"    - Push the changes to origin\n"
            )
        )
        self.confirm_or_abort()
        self.safe_execute("git add .")
        try:
            subprocess.call(f'git commit -m "{message}"', shell=True)
        except subprocess.CalledProcessError:
            pass

        self.execute_first_success(
            "git push", f"git push --set-upstream origin {current_branch()}"
        )

    def open(self):
        """ Open an issue in the Google Chrome browser. """

    def pull_request(self, base_branch: str):
        """ Create a GitHub Pull Request for the specified branch. """

    # Helpers

    def _config_init(self):
        """ Initialize the config values for this Git repository. """
        self.echo(
            f"In order to retrieve the issue info we need the issue tracker API.\n"
            f"Examples:\n"
            f"    - GitHub: https://api.github.com/repos/:owner/:repo/issues\n"
        )
        self._config.issue_tracker_api = click.prompt(
            "Enter the API URL for your issue tracker", type=str
        )
        self._config.save()

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

    def execute_or_abort(self, command: str):
        """ Execute a command on the terminal and abort if error occurs. """
        try:
            self.execute(command)
        except subprocess.CalledProcessError as e:
            self.log(e)
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
        url = f"{self._config.issue_tracker_api.strip('/')}/{issue_id}"
        issue_tracker = self._config.issue_tracker()
        auth = None
        if self._config.issue_tracker_is_github() and os.getenv("MGIT_GITHUB_USERNAME"):
            auth = (
                (os.getenv("MGIT_GITHUB_USERNAME"), os.getenv("MGIT_GITHUB_API_TOKEN")),
            )
        try:
            res = requests.get(
                url, headers={"content-type": "application/json"}, auth=auth
            )
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # TODO: Determine how to get the ENV vars to persist.
            # if '401 Client Error: Unauthorized' in str(e):
            #      username = click.prompt(f'Please enter your {issue_tracker} username', type=str)
            #      token = click.prompt(f'Please enter your {issue_tracker} API token', type=str, hide_input=True)
            #      auth=(
            #          os.getenv("MGIT_GITHUB_USERNAME"),
            #          os.getenv("MGIT_GITHUB_API_TOKEN"),
            #      ),
            # else:
            raise e
        title = ""
        if self._config.issue_tracker_is_github():
            title = res.json()["title"]
        return Issue(issue_id, title)

    def get_issue_or_abort(self, issue_id: str) -> Issue:
        """ Get the issue by ID or exit the program. """
        try:
            return self.get_issue(issue_id)
        except requests.exceptions.HTTPError as e:
            self.log(e)
            sys.exit(1)

    # Click Helpers

    def echo(self, message: str):
        """ Echo a message to the terminal. """
        click.echo(message)

    def confirm_or_abort(self):
        """ Abort unless the user confirms that they wish to continue. """
        click.confirm("Do you wish to continue?", abort=True)

    def confirm(self, message="Do you wish to continue?", abort=False) -> bool:
        """ Get user confirmation. """
        return click.confirm(message, abort=abort)

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
