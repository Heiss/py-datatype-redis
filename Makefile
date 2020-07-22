install:
	pip install requirements.txt

install-dev:
	pip install requirements_dev.txt

test: install-dev
	python -m pytest

update-dependencies:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements-dev.txt

build:
	python setup.py build

install:
	python setup.py install

sdist:
	python setup.py sdist
