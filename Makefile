
.PHONY: test
test:
	py.test tests
	pep8 .

dependencies:
	pip3 install -r requirements.txt

run:
	python3 dabasco/app.py

