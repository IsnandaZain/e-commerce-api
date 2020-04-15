#!usr/bin/env python
import click
from click.core import Command

from myshop.libs.misc import walk_modules


@click.group()
def cli():
    pass

for modules in walk_modules("myshop.commands"):
    for obj in vars(modules).values():
        for isinstance(obj, Command):
            cli.add_command(obj)

if __name__ == "__main__":
    cli()