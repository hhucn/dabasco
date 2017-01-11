test:
	py.test tests
	pep8 .

dependencies:
	pip install -r requirements.txt

run:
	python doj/app.py

.PHONY: test