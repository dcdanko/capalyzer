
import click

from capalyzer.packet_builder.cli import all_tables, cli_make_read_stats, long_taxa
from capalyzer.packet_parser.cli import diversity, cli_annotate_taxa


@click.group()
def main():
    pass


main.add_command(all_tables)
main.add_command(cli_make_read_stats)
main.add_command(diversity)
main.add_command(long_taxa)
main.add_command(cli_annotate_taxa)

if __name__ == '__main__':
    main()
