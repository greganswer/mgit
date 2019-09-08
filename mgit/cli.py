import click


# TODO: Extract to separate file.
class CustomMultiCommand(click.Group):
    def command(self, *args, **kwargs):
        """
        Behaves the same as `click.Group.command()` except if passed
        a list of names, all after the first will be aliases for the first.

        Reference: https://stackoverflow.com/a/46721013
        """

        def decorator(f):
            if args and isinstance(args[0], list):
                _args = [args[0][0]] + list(args[1:])
                for alias in args[0][1:]:
                    cmd = super(CustomMultiCommand, self).command(
                        alias, *args[1:], **kwargs
                    )(f)
                    cmd.short_help = f"Alias for {_args[0]}."
            else:
                _args = args
            cmd = super(CustomMultiCommand, self).command(*_args, **kwargs)(f)
            return cmd

        return decorator


@click.group(
    cls=CustomMultiCommand, context_settings={"help_option_names": ["-h", "--help"]}
)
# TODO: Improve help message.
@click.option("--verbose", "-v", is_flag=True, help="Show detailed logs.")
@click.pass_context
def cli(ctx, verbose):
    """
    Run Git work flows for GitHub with issue tracking ticket numbers.
    """
    # Ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block add the end of the file)
    ctx.ensure_object(dict)
    ctx.obj = {
        # 'app': App(verbose=verbose),
    }


# TODO: Show example in documentation.
@click.argument("issue_id")
@click.option("-b", "--base-branch", help="The base branch to perform this action on.")
@cli.command()
@click.pass_context
def branch(ctx, issue_id: str, base_branch: str):
    """
    Create a branch using issue ID and title.

    The new branch name is taken from the title of the issue found.
    The new branch is created off of the --base-branch or the default base branch.

    NOTE: User confirmation is required before the branch is created.
    """
    # ctx['app'].branch(issue_id, base_branch)
    click.echo("Branch command")


# TODO: Show example in documentation.
@click.option("-m", "--message", help="The commit message.")
@cli.command()
@click.pass_context
def commit(ctx, message: str):
    """
    Create a commit and push to GitHub.

    All of the un-staged files are added, committed and pushed to GitHub.
    The commit message is extracted from the branch name if one is not supplied
    using the --message option.

    NOTE: User confirmation is required before the commit is created.
    """
    # ctx['app'].commit(message)
    click.echo("commit command")


@cli.command()
@click.pass_context
def open(ctx):
    """
    Open an issue in the Google Chrome browser.
    """
    # ctx['app'].commit(message)
    click.echo("open command")


@cli.command(['pull-request', 'pr'])
@click.option("-b", "--base-branch", help="The base branch to perform this action on.")
@click.pass_context
def pull_request(ctx):
    """
    Create a GitHub Pull Request for the specified branch.

    NOTE: User confirmation is required before the pull request is created.
    """
    # ctx['app'].commit(message)
    click.echo("pull request command")


if __name__ == "__main__":
    cli()