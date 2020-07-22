build:
	python setup.py build

install:
	python setup.py install

install-dev:
	pip install requirements_dev.txt

test: install-dev
	python -m pytest

update-dependencies:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

sdist:
	python setup.py sdist

clean:
	rm -r dist *.egg-info
