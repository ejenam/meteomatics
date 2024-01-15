install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv meteo.py

format:
	black *.py

lint:
	pylint --disable=R,C meteo.py

run:
	python meteo.py

all: install lint test