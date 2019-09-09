import click
import subprocess


class App:
    def __init__(self, verbose=False):
        self.verbose = verbose

    def branch(self, issue_id: str, base_branch: str):
        """ Create a branch using issue ID and title. """

    def commit(self, message: str):
        """ Create a commit and push to GitHub. """

    def open(self):
        """ Open an issue in the Google Chrome browser. """

    def pull_request(self, base_branch: str):
        """ Create a GitHub Pull Request for the specified branch. """

    # Helpers

    def execute_command(self, command: str):
        """ Execute a command on the terminal. """
        return subprocess.check_output(command.split())

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

    # Colors

    def blue(self, message, bold=False):
        return click.style(message, fg="blue", bold=bold)

    def green(self, message, bold=False):
        return click.style(message, fg="green", bold=bold)

    def red(self, message, bold=False):
        return click.style(message, fg="red", bold=bold)

    def yellow(self, message, bold=False):
        return click.style(message, fg="yellow", bold=bold)
