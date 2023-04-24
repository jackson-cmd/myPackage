"""A works class for bibtex utilities."""
import click
from .works import Works


@click.option("--flag", default="ris", help="Number of greetings.")
@click.command(help="OpenAlex Institutions")
@click.argument("query", nargs=-1)
def main(flag, query):
    """A main fucntion for bibtex utilities."""
    works = Works(query[0])
    if flag == "ris":
        print(works.ris)
    elif flag == "bibtex":
        print(works.bibtex)
