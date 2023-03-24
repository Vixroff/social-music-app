# Build #

## Localhost ##

### requirements: ###

- MySQL server
- Python 3.9^

### set up: ##
1) Pull source code from GitHub repository:
```
git clone https://github.com/Vixroff/social-music-app.git
```
2) Activate env and install dependencies:
```
python3 -m venv env
source env/bin/activate
pip install requirements.txt
```

3) Go to https://developer.musixmatch.com/ and get your personal API KEY

4) Create '.env' file and add your personal variables (DB_HOST is constant):
```
DB_HOST = localhost

SECRET_KEY = 'your-secret-key'
DB_USER = 'your-db-username'
DB_PASSWORD = 'your-db-password'
DB_NAME = 'db-name'
DB_PORT = 'db-port'
MUSIXMATCH_API = 'your-api-key-from-musixmatch'
```

5) Activate MySQL server and Create database with command below:
```
python -m db
```

6) Execute migrations:
```
python manage.py migrate
```

7) Run server by command below and go to http://127.0.0.1:8000
```
make run
```

## Docker compose ##

### requirements ###
- Docker

### set up ###
1) Pull source code from GitHub repository:
```
git clone https://github.com/Vixroff/social-music-app.git
```

2) Create '.env' file and add your personal variables (DB_HOST is constant):
```
DB_HOST = mysql

SECRET_KEY = 'your-secret-key'
DB_USER = 'your-db-username'
DB_PASSWORD = 'your-db-password'
DB_NAME = 'db-name'
DB_PORT = 'db-port'
MUSIXMATCH_API = 'your-api-key-from-musixmatch'
```

3) Build and run container (!Note: sometimes there is trouble with running queue of mysql and app containers. To solve it run app container manually after command):
```
docker-compose -p social-music-app up -d
```
