all: clean clean-pyc test

clean: clean-pyc
	rm -rf build
	rm -rf dist
	rm -rf *.egg
	rm -rf *.egg-info
	find . -name '.DS_Store' -delete
	rm -rf tests/__pycache__

clean-pyc:
	find . -name '*.pyc' -delete
	find . -name '*.pyo' -delete
	find . -name '*~' -delete
	find . -name '*,cover' -delete

test:
	py.test -x tests/

testcov:
	py.test --cov-config .coveragerc --cov allspeak tests/

coverage:
	py.test --cov-config .coveragerc --cov-report html --cov allspeak tests/

publish: clean
	python setup.py sdist upload

