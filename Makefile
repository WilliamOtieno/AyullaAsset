help:
	echo "make setup -> Set up Project with its dependencies\nmake run -> Activate Virtual ENV and run server\nmake test -> Run all tests\nmake coverage -> Test Coverage Report"

setup:
	python3 -m venv venv
	. venv/bin/activate
	pip install -r requirements.txt
	python manage.py migrate

run:
	. venv/bin/activate
	python manage.py migrate
	python manage.py runserver

test:
	coverage run manage.py test

coverage:
	coverage report

