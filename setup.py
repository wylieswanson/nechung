#!/usr/bin/env python
from glob import glob
from distutils.core import setup

setup(
	name="nechung",
	version="0.2",
	description="Agile Cloud Nechung Mutator Workflow",
	keywords=['nechung'],
	author="Wylie Swanson",
	author_email="wylie@pingzero.net",
	url="http://www.pingzero.net",
	license="GPLv3",
	package_dir={'': 'src'},
	packages=[''],
	scripts=glob("bin/*"),
	)
