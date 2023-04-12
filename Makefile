# Create targets

.ONESHELL:
SHELL = /bin/bash

create_environment :
	source /srv/conda/etc/profile.d/conda.sh
	conda env create -f environment.yml 
	conda activate notebook
	conda install ipykernel
	python -m ipykernel install --user --name make-env --display-name "IPython - Make"


html:
	jupyter-book build .

## clean             : Remove output files
.PHONY : clean

clean:
	rm -rf figures
	rm -rf audio 
	rm -rf _build/html/
	rm -rf _build