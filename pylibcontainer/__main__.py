from __future__ import print_function
from pylibcontainer import image
import click

@click.group()
def pylibcontainer():
    pass

pylibcontainer.add_command(image.run)

if __name__ == "__main__":
    pylibcontainer()
