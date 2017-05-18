test:
	py.test tests
	pep8 .

dependencies:
	pip install -r requirements.txt

run:
	python dabasco/app.py

.PHONY: test