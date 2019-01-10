
import click

from capalyzer.packet_builder.cli import all_tables


@click.group()
def main():
    pass


main.add_command(all_tables)


if __name__ == '__main__':
    main()
