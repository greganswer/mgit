import subprocess
import click
import sys
import os


def call(command, abort=True, shell=False, verbose=False):
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
