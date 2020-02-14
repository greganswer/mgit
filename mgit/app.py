import click  # https://click.palletsprojects.com/en/7.x/
import subprocess
import sys
import requests
import json
import os
import shlex
import shutil
import webbrowser

from mgit import git
from mgit import configs
from .translator import Translator
from mgit import issues


class App:
    def __init__(
        self, log_file, verbose: bool, config=configs.Config(), translator=Translator()
    ):
        """
        Initialize the app by validating the environment.

        :param log_file: The file where log output is sent.
        :param verbose: Determine if additional info should be logged.
        :param config: mgit configuration object.
        :param translator: Translator object.
        """
        self._log_file = log_file
        self._verbose = verbose
        self._config = config
        self._translator = translator

        # Validate there is a .git folder
        if not git.initialized():
            self.abort(self._translator.invalid_git_directory())

        # Prompt the user for config values if the project mgit.json file does not exist.
        if not configs.loaded():
            self._config_init()

    def branch(self, issue_id: str, base_branch: str):
        """ Create a branch using issue ID and title. """
        # TODO: Validate Inputs
        #   - username present in os.getenv("MGIT_GITHUB_USERNAME") or similar
        #   - token present in os.getenv("MGIT_GITHUB_API_TOKEN") or similar

        if not base_branch:
            base_branch = git.default_base_branch()

        try:
            new_branch = issues.from_tracker(issue_id, self._config).branch_name
        except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
            self.abort(e)

        self.echo(self._translator.create_branch_warning(base_branch, new_branch))
        self.confirm_or_abort()
        git.create_branch(base_branch, new_branch)

    def commit(self, message: str, issue_id: str):
        """ Create a commit and push to GitHub. """
        issue = None
        if not message:
            try:
                if issue_id:
                    issue = issues.from_tracker(issue_id)
                else:
                    issue = issues.from_branch(
                        git.current_branch(), config=self._config
                    )

                message = str(issue)
                if self._config.issue_tracker_is_github:
                    message += self._translator.closes_issue_id(issue.id)

            except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
                self.abort(e)

            except ValueError:
                self.abort(
                    self._translator.branch_has_no_issue_id(git.current_branch())
                )

        self.echo(self._translator.commit_warning(message))
        self.confirm_or_abort()
        git.commit_all(message)
        git.push(git.current_branch())

    def open(self):
        """ Open an issue in the user's default browser. """
        issue = issues.from_branch(git.current_branch(), config=self._config)
        webbrowser.open(issue.url)

    def pull_request(self, base_branch: str):
        """ Create a GitHub Pull Request for the specified branch. """
        if not base_branch:
            base_branch = git.default_base_branch()

        issue = issues.from_branch(git.current_branch())
        title = message = issue.title
        if issue and self._config.issue_tracker_is_github:
            message += f"\n\nCloses #{issue.id}"

        self.echo(self._translator.pull_request_warning(message, base_branch, title))
        self.confirm_or_abort()
        git.commit_all(message)

        self.echo(self._translator.update_base_branch_confirmation(base_branch))
        if self.confirm():
            git.rebase(base_branch)
            git.push(git.current_branch())

        body = self._translator.pull_request_body(
            title, self._config.issue_tracker, issue.id, issue.url
        )
        try:
            assignee = self.execute("git config --global user.handle")
        except subprocess.CalledProcessError:
            assignee = ""

        git.pull_request()
        self.execute_hub_command(
            f'pull-request -fpo -b {base_branch} -m "{body}" -a {assignee}'
        )
        self.safe_execute("git push")

    # # Helpers

    def _config_init(self):
        """ Initialize the config values for this Git repository. """
        self.echo(self._translator.init_issue_tracker_api())
        self._config.issue_tracker_api = click.prompt(
            self._translator.issue_tracker_api_prompt(), type=str
        )
        self._config.save()

    # TODO: Try to use this method instead of the 3 below.
    # TODO: Rename to `execute` once ready.
    def execute_prime(self, command: str, abort=True):
        """ Execute a command on the terminal and log errors to log file. """
        try:
            if self._verbose:
                self.log(f"Executing command -> {command}")
            return subprocess.check_output(
                shlex.split(command), stderr=self._log_file
            ).decode("utf-8")
        except subprocess.CalledProcessError as e:
            if abort:
                self.abort(e, e.returncode)

    # TODO: replace aborts with this
    def abort(self, message, code=1):
        self.log(message)
        sys.exit(code)

    def execute_hub_command(self, command):
        """
        Execute a command using the Hub CLI.

        :param command: The command hub will execute.
        """
        hub_installed = shutil.which("hub")
        if not hub_installed:
            self.abort(self._translator.hub_cli_missing())
        try:
            subprocess.call(f"hub {command}", shell=True)
        except subprocess.CalledProcessError as e:
            self.abort(e, e.returncode)

    # Click Helpers

    def echo(self, message: str):
        """ Echo a message to the terminal. """
        click.echo(message)

    # TODO: Remove this duplicate method
    def confirm_or_abort(self):
        """ Abort unless the user confirms that they wish to continue. """
        click.confirm("Do you wish to continue?", abort=True)

    def confirm(self, message="Do you wish to continue?", abort=False) -> bool:
        """ Get user confirmation. """
        return click.confirm(message, abort=abort)

    def log(self, message: str):
        """ Log message to the log_file. """
        # TODO: Delete one
        click.echo(message)
        click.echo(message, file=self._log_file)
