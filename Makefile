# Create targets

env: 
	conda create -n ligo python=3.8
	conda activate ligo
	python -m ipykernel install --user --name ligo --display-name "IPython - ligo"
# conda env export --from-history > environment.yml

html:
	

clean:
	rm -r figures 
	rm -r audio 
	rm -r _build