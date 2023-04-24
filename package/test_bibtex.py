"""A package for bibtex utilities testing."""
from pkg import Works

A = "@article{kitchin-2015,\n DATE_ADDED = {2023-04-16T17:13:17.193190},\n "
B = "author = {John R. Kitchin},\n doi = {https://doi.org/10.1021/acscatal.5b00538},\n "
C = "journal = {American Chemical Society},\n number = {6},\n pages = {3894-3899},\n "
D = "title = {Examples of Effective Data Sharing in Scientific Publishing},\n url = "
E = "{https://doi.org/10.1021/acscatal.5b00538},\n volume = {5},\n year = {2015}\n}\n"
REF = A + B + C + D + E


def test_bibtex():
    """A class to test bibtex."""
    works = Works("https://doi.org/10.1021/acscatal.5b00538")
    assert REF == works.bibtex
