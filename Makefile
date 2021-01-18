.PHONY: clean test run

_version=$(strip $(shell sed -n -e "s/version[\s\t]*=[\s\t]*'\([0-9.]\+\)',/\1/p" -e "s/^[[:space:]]*//" setup.py))

clean:
	rm -rf ./dist
	rm -rf *.egg-info

dist: clean
	./venv/bin/python setup.py sdist

dep: clean
	rm -rf ./venv
	virtualenv --python=python3.8 ./venv
	./venv/bin/pip install .
	./venv/bin/pip uninstall -y flask_signature_auth
	./venv/bin/pip freeze > requirements.txt
	./venv/bin/pip install autopep8 flask_testing
	./venv/bin/pip freeze > requirements-dev.txt
	
test:
	FLASK_ENV=development ./venv/bin/python -m unittest -v