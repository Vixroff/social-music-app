## Set up ##
1) Activate MySQL server and Create database

2) Activate env and Install dependencies:
```
python3 -m venv env
source env/bin/activate
pip install requirements.txt
```

3) Go to https://developer.musixmatch.com/ and get your personal API KEY

4) Create .env file and add your personal variables:
    ```
    SECRET_KEY = 'your-secret-key'
    DB_USER = 'your-db-username'
    DB_PASSWORD = 'your-db-password'
    DB_NAME = 'db-name'
    DB_HOST = 'db-host'
    DB_PORT = 'db-port'
    MUSIXMATCH_API = 'your-api-key-from-musixmatch'
    ```

5) Execute migrations to your db:
```
python manage.py migrate
```

6) Run server by command below and go to 127.0.0:8000
```
make run
```
