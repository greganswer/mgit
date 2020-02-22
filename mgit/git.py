import subprocess
import os
import click
import sys
import shutil

from mgit import execute
from mgit import translator

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


def create_branch(base_branch: str, new_branch: str):
    """ Create a new branch off a base branch. """
    subprocess.call(["git", "checkout", base_branch])
    subprocess.call(["git", "pull"])
    subprocess.call(["git", "checkout", "-b", new_branch])


def rebase(base_branch: str):
    """ Rebase off a base branch. """
    subprocess.call(["git", "checkout", base_branch])
    subprocess.call(["git", "pull"])
    subprocess.call(["git", "checkout", "-"])
    subprocess.call(["git", "rebase", "-i", base_branch])


def commit_all(message: str):
    """ Add all files and commit. Ignores errors. """
    execute.call(["git", "add", "."], abort=False)
    execute.call(f'git commit -m "{message}"', abort=False, shell=True)


def push(branch=None):
    """ Push the changes to the remote branch. Ignores errors. """
    if not branch:
        branch = default_base_branch()

    execute.call(["git", "push", "-f"], abort=False)
    execute.call(["git", "push", "--set-upstream", "origin", branch], abort=False)


def assignee() -> str:
    """ Get the assignee or empty string. """
    return execute.output(["git", "config", "--global", "user.handle"], abort=False)


# GitHub


def hub_installed() -> bool:
    """ Determine `hub` CLI tool is installed. """
    return shutil.which("hub")


def pull_request(base_branch: str, body: str):
    """ Create a pull request on GitHub """
    if not hub_installed():
        raise HubCLIMissing()

    execute.call(
        f'hub pull-request -fpo -b {base_branch} -m "{body}" -a {assignee()}',
        shell=True,
    )

