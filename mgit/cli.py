import click  # https://click.palletsprojects.com/en/7.x/
import sys

from .app import App
from ._version import __version__

# TODO: rename function to mgit
@click.group(name="mgit", context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "--log-file",
    "-l",
    type=click.File("w"),
    default=sys.stderr,
    show_default="stderr",
    help="File to log errors and warnings.",
)
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose mode.")
@click.version_option(version=__version__, message="%(prog)s version %(version)s")
@click.pass_context
def cli(ctx, log_file, verbose):
    """
    Run Git work flows for GitHub with issue tracking ticket numbers.
    """
    ctx.obj = App(log_file=log_file, verbose=verbose)


@click.argument("issue_id")
@click.option("-b", "--base-branch", help="The base branch to perform this action on.")
@cli.command()
@click.pass_obj
def branch(app, issue_id: str, base_branch: str):
    """
    Create a branch using issue ID and title.

    The new branch name is taken from the title of the issue found.
    The new branch is created off of the --base-branch or the default base branch.

    \b
    NOTE
        User confirmation is required before the branch is created.

    \b
    EXAMPLES
        $ mgit branch JIR-123
        $ mgit branch JIR-123 --base-branch develop
    """
    app.branch(issue_id, base_branch)


@click.option("-m", "--message", help="The commit message.")
@click.option("--issue-id", "--id", help="The ID of the issue being worked on.")
@cli.command()
@click.pass_obj
def commit(app, message: str, issue_id: str):
    """
    Create a commit and push to GitHub.

    All of the un-staged files are added, committed and pushed to GitHub.
    The commit message is extracted from the branch name if one is not supplied
    using the --message option.

    \b
    NOTE
        User confirmation is required before the commit is created.

    \b
    EXAMPLES
        $ mgit commit
        $ mgit commit --message 'Update different from title'
    """
    app.commit(message, issue_id)


@cli.command()
@click.pass_obj
def open(app):
    """ Open an issue in the Google Chrome browser. """
    app.open()


@cli.command()
@click.option("-b", "--base-branch", help="The base branch to perform this action on.")
@click.pass_obj
def pr(app, base_branch=None):
    """
    Create a GitHub Pull Request for the specified branch.

    \b
    NOTE
        User confirmation is required before the pull request is created.

    \b
    EXAMPLES
        $ mgit pull-request
        $ mgit pull-request --base-branch develop
    """
    app.pr(base_branch)


if __name__ == "__main__":
    cli()
