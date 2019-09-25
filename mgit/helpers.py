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


class Mutex(click.Option):
    """
    Reference: https://github.com/pallets/click/issues/257#issuecomment-403312784
    """

    def __init__(self, *args, **kwargs):
        self.not_required_if: list = kwargs.pop("not_required_if")

        assert self.not_required_if, "'not_required_if' parameter required"
        kwargs["help"] = (
            kwargs.get("help", "")
            + " Option is mutually exclusive with "
            + ", ".join(self.not_required_if)
            + "."
        ).strip()
        super(Mutex, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_opt: bool = self.name in opts
        for mutex_opt in self.not_required_if:
            if mutex_opt in opts:
                if current_opt:
                    raise click.UsageError(
                        "Illegal usage: '"
                        + str(self.name)
                        + "' is mutually exclusive with '"
                        + str(mutex_opt)
                        + "'."
                    )
                else:
                    self.prompt = None
        return super(Mutex, self).handle_parse_result(ctx, opts, args)
