[metadata]
name             = ligotools
version          = attr:ligotools.__version__
author           = Ligo Scientific Collaboration (LSC) and Group 15: Jennifer, Yi, Irene, Zac
author_email     = jenniferr.brown@berkeley.edu
description      = A Python library for Ligotools
long_description = file: README.md, LICENSE
long_description_content_type = text/markdown
keywords         = tools
license          = BSD 3-Clause License
classifiers      =
	Programming Language :: Python :: 3
    License :: OSI Approved :: BSD License
    Operating System :: OS Independent

[options]
include_package_data = True
packages = find:
# These should be consistent with what is specified in the environment.yml
python_requires  = >= 3.6,
install_requires =
	tqdm

[options.packages.find]
exclude =
    examples*
    docs*