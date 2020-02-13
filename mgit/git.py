import subprocess
import os
import click
import sys


# TODO: Add proper docstring format
#       ref: https://realpython.com/documenting-python-code/#docstring-formats

DEFAULT_BASE_BRANCHES = ["dev", "develop", "development", "master"]


def initialized() -> bool:
    """ Determine if current directory is a Git repo. """
    return os.path.isdir(".git")


def current_branch() -> str:
    """ Get current branch for the current Git repo. """
    output = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return str(output, "utf-8").strip("\n")


def default_base_branch() -> str:
    """ Return the default base branch for the current Git repo. """
    for branch in DEFAULT_BASE_BRANCHES:
        if branch_exists(branch):
            return branch


def branch_exists(branch: str) -> bool:
    """ Check if the branch exists in the current Git repo. """
    try:
        subprocess.check_call(
            ["git", "rev-parse", "--quiet", "--verify", branch],
            stdout=subprocess.DEVNULL,
        )
        return True
    except subprocess.CalledProcessError:
        return False


def new_branch_off(base_branch: str, new_branch: str):
    """ Create a new branch off a base branch. """
    subprocess.call(["git", "checkout", base_branch])
    subprocess.call(["git", "pull"])
    subprocess.call(["git", "checkout", "-b", new_branch])


def rebase_off_branch(base_branch: str):
    """ Rebase off a base branch. """
    subprocess.call(["git", "checkout", base_branch])
    subprocess.call(["git", "pull"])
    subprocess.call(["git", "checkout", "-"])
    subprocess.call(["git", "rebase", "-i", base_branch])


def commit_all(message: str):
    """ Add all files and commit. Ignores errors. """
    execute_call(["git", "add", "."], abort=False)
    execute_call(f'git commit -m "{message}"', shell=True)


def push(branch: str):
    """ Push the changes to the remote branch. Ignores errors. """
    execute_call(["git", "push", "-f"], abort=False)
    execute_call(["git", "push", "--set-upstream", "origin", branch], abort=False)


# TODO: Extract Duplicate Function
def execute_call(command, abort=True, shell=False, verbose=False):
    """ Execute `subprocess.call`.

    Raises
    ------
    subprocess.CalledProcessError
        If the commands fail and `abort` is True.
    """
    try:
        if verbose:
            click.echo(command)
        subprocess.call(command, shell=shell)
    except subprocess.CalledProcessError as e:
        if abort:
            click.echo(e)
            sys.exit(e.returncode)
