build:
	python setup.py build

install:
	pip install -r requirements.txt | grep -v 'already satisfied' || true

install-dev:
	pip install -r requirements_dev.txt | grep -v 'already satisfied' || true

test: install install-dev
	python -m pytest --cov=datatype_redis --cov-report xml

update-dependencies:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements_dev.txt

sdist:
	python setup.py sdist

clean:
	rm -r dist src/*.egg-info build .coverage coverage.xml .pytest_cache
