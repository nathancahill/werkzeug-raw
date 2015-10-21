.PHONY: docs

init:
	pip install -r requirements.txt

test:
	nosetests --with-coverage --cover-package=werkzeug_raw

docs:
	cd docs && make html
