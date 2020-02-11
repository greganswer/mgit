import subprocess

DEFAULT_BASE_BRANCHES = ["dev", "develop", "development", "master"]


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
