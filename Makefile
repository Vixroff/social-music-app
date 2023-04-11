run:
	poetry run python app/manage.py runserver

migrate:
	poetry run python app/manage.py makemigrations 
	poetry run python app/manage.py migrate
