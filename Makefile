run:
	python manage.py runserver

migrate:
	python manage.py migrate

make install:
	pip install -r requirements.txt

shell:
	python manage.py shell

migrations:
	python manage.py makemigrations

build: install migrations migrate run
