run:
	poetry run python musicapp/manage.py runserver

migrate:
	poetry run python musicapp/manage.py makemigrations 
	poetry run python musicapp/manage.py migrate

test:
	poetry run python musicapp/manage.py test app --verbosity=2
