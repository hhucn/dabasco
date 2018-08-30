
.PHONY: test
test:
	cd dabasco && nosetests --with-coverage dabasco

dependencies:
	pip3 install -r requirements.txt

run:
	python3 dabasco/app.py

