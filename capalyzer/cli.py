
import click

from capalyzer.packet_builder.cli import all_tables
from capalyzer.packet_parser.cli import diversity


@click.group()
def main():
    pass


main.add_command(all_tables)
main.add_command(diversity)


if __name__ == '__main__':
    main()
