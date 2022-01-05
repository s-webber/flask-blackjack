Create virtual environment:

```
python -m venv venv
```

On Windows:

```
venv\Scripts\activate
```

On Linux:

```
source venv/bin/activate
```

Install dependencies:

```
python -m pip install flask
python -m pip install pytest
python -m pip install pytest-mock
python -m pip install coverage
python -m pip install sphinx
```

Run unit-tests:

```
pytest tests
```

Run unit-tests and generate code coverage reports:

```
coverage run --source=blackjack -m pytest
```

To view code coverage:

```
coverage report -m
```

To generate code coverage report as HTML run:

```
coverage html
```

Report will be available at: `htmlcov/index.html`

To generate documentation:

```
cd docs
make html
```

Documentation will be available at: `docs/_build/html/index.html`

On Windows:

```
set FLASK_APP=blackjack.app
```

On Linux:

```
export FLASK_APP=blackjack.app
```

To run server:

```
flask run
```

See:

https://coverage.readthedocs.io/en/coverage-5.1/
https://www.sphinx-doc.org/en/master/usage/quickstart.html
