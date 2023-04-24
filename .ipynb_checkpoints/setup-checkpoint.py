"""A package for bibtex utilities."""

from setuptools import setup

setup(
    name="package",
    version="0.0.1",
    description="OpenAlex utilities",
    maintainer="Mengxiao Wang",
    maintainer_email="mengxiaw@andrew.cmu.edu",
    license="MIT",
    packages=["package"],
    entry_points={"console_scripts": ["oa = package.main:main"]},
    scripts=[],
    long_description="""A set of OpenAlex utilities""",
)
