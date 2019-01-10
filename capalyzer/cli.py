
import click

from capalyzer.packet_builder.cli import tables


@click.group()
def main():
    pass


main.add_command(tables)


if __name__ == '__main__':
    main()
