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
from mgit import translator
from mgit import issues


class App:
    def __init__(
        self,
        log_file,
        verbose: bool,
        config=configs.Config(),
        translator=translator.Translator(),
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

        # TODO: Write a test for when the user says no.
        self.echo(self._translator.create_branch_warning(base_branch, new_branch))
        self.confirm(abort=True)
        git.create_branch(base_branch, new_branch)

    def commit(self, message: str, issue_id: str):
        """ Create a commit and push to GitHub. """
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
                    # TODO: Ask the user if this issue is being closed
                    # message += self._translator.closes_issue_id(issue.id)
                    pass

            except (requests.exceptions.HTTPError, requests.exceptions.Timeout) as e:
                self.abort(e)

            except ValueError:
                self.abort(
                    self._translator.branch_has_no_issue_id(git.current_branch())
                )

        # TODO: Write a test for when the user says no.
        self.echo(self._translator.commit_warning(message))
        self.confirm(abort=True)
        git.commit_all(message)
        git.push(git.current_branch())

    def open(self):
        """ Open an issue in the user's default browser. """
        issue = issues.from_branch(git.current_branch(), config=self._config)
        webbrowser.open(issue.url)

    def pr(self, base_branch: str):
        """ Create a GitHub Pull Request for the specified branch. """
        if not git.hub_installed():
            self.abort(translator.MESSAGES["hub_cli_missing"])

        if not base_branch:
            base_branch = git.default_base_branch()

        # Create title and message from current branch info.
        try:
            issue = issues.from_branch(git.current_branch())
            title = message = issue.title
            if self._config.issue_tracker_is_github:
                message += f"\n\nCloses #{issue.id}"
        except ValueError:
            self.abort(self._translator.branch_has_no_issue_id(git.current_branch()))

        # Prompt user to commit all changes.
        # TODO: Write a test for when the user says no.
        self.echo(self._translator.pull_request_warning(message, base_branch, title))
        self.confirm(abort=True)
        git.commit_all(message)

        # Prompt user to update the current branch.
        # TODO: Write a test for when the user says no.
        self.echo(self._translator.update_base_branch_confirmation(base_branch))
        if self.confirm():
            git.rebase(base_branch)
            git.push(git.current_branch())

        # Make the pull request and push the changes to the remote branch.
        try:
            body = self._translator.pull_request_body(
                title, self._config.issue_tracker, issue.id, issue.url
            )
            git.push()
            git.pull_request(base_branch, body)

        except subprocess.CalledProcessError as e:
            self.abort(e)

    # # Helpers

    def _config_init(self):
        """ Initialize the config values for this Git repository. """
        self.echo(self._translator.init_issue_tracker_api())
        self._config.issue_tracker_api = click.prompt(
            self._translator.issue_tracker_api_prompt(), type=str
        )
        self._config.save()

    def abort(self, message, code=1):
        self.echo(message)
        sys.exit(code)

    # Click Helpers

    def echo(self, message: str):
        """ Echo a message to the terminal. """
        click.echo(message)

    def confirm(self, message="Do you wish to continue?", abort=False) -> bool:
        """ Get user confirmation. """
        return click.confirm(message, abort=abort)
