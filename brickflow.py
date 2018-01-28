import click
from pprint import PrettyPrinter

from core import Plan


@click.command()
@click.option('--layout', type=click.Choice(['neato', 'dot', 'twopi', 'circo', 'fdp', 'nop']), default='neato')
@click.option('--format', type=click.Choice(['gif', 'jpeg', 'pdf', 'png', 'svg']), default=None)
@click.argument('data', type=click.Path(exists=True))
@click.argument('output', type=click.Path(exists=False))
def cli(layout, format, data, output):
    p = Plan()
    p.load(data)
    #if p.validate():
    #    pp = PrettyPrinter(indent=4)
    #    pp.pprint({'groups': p.to_topological_dict()})
    p.plot(output, layout=layout, format=format)


if __name__ == '__main__':
    cli()
