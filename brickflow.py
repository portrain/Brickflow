import click
from pprint import PrettyPrinter

from core import Plan

_version = '0.1.0'


@click.group(context_settings=dict(help_option_names=['-h', '--help']))
@click.version_option(version=_version)
def cli():
    pass


@cli.command('plot')
@click.option('--layout', type=click.Choice(['neato', 'dot', 'twopi', 'circo', 'fdp', 'nop']), default='neato')
@click.option('--format', type=click.Choice(['gif', 'jpeg', 'pdf', 'png', 'svg']), default=None)
@click.argument('data', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
def cli_plot(layout, format, data, output):
    """ Plot build plan as a graph to an image file """
    p = Plan()
    p.load(data)
    if p.validate():
        p.plot(output, layout=layout, format=format)
        click.echo(f'File written to {output}')
    else:
        click.echo('The input file is not valid')


@cli.command('validate')
@click.argument('data', type=click.Path(exists=True))
def cli_validate(data):
    """ Validate the build plan """
    p = Plan()
    p.load(data)
    if p.validate():
        click.echo('The input file is valid')
    else:
        click.echo('The input file is not valid')


@cli.command('print')
@click.argument('data', type=click.Path(exists=True))
def cli_print(data):
    """ Print a topological sorted build plan """
    p = Plan()
    p.load(data)
    if p.validate():
        pp = PrettyPrinter(indent=4)
        pp.pprint({'groups': p.to_topological_dict()})
    else:
        click.echo('The input file is not valid')


if __name__ == '__main__':
    cli()
