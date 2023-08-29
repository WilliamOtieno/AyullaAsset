help:
	echo "make setup -> Set up Project with its dependencies\nmake run -> Activate Virtual ENV and run server\nmake test -> Run all tests\nmake coverage -> Test Coverage Report"

setup:
	python3 -m venv venv
	. venv/bin/activate
	venv/bin/pip install -r requirements.txt
	venv/bin/python manage.py migrate


run:
	. venv/bin/activate
	venv/bin/python manage.py migrate
	venv/bin/python manage.py runserver

test:
	venv/bin/coverage run manage.py test

coverage:
	venv/bin/coverage report

