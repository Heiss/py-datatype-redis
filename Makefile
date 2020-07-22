build:
	python setup.py build

install:
	python setup.py install

install-dev:
	pip install -r requirements_dev.txt

test: install-dev
	python -m pytest --cov=datatype_redis --cov-report xml

update-dependencies:
	pipenv update
	pipenv lock -r > requirements.txt
	pipenv lock -r -d > requirements_dev.txt

sdist:
	python setup.py sdist

clean:
	rm -r dist *.egg-info
