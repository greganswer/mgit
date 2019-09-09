import click


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
