import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bamToBigWig",
    version = "0.1.BETA",
    author = "Panos Firmpas",
    author_email = "panosfirbas@gmail.com",
    description = ("Create a bigwig file with signal derived from a sorted and indexed bam file."),
    license = "GPL3",
    keywords = "bam bigwig",
    url = "https://github.com/PanosFirmpas/bamToBigWig",
    packages=[''],
    install_requires=['numpy', 'pysam'],
    long_description=read('README'),
    scripts=['scripts/bamToBigWig'],
    classifiers=[
        "Development Status :: Beta",
        "Topic :: Utilities"
    ],
)
