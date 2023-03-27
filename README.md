
## **Build** ##

There are several ways to build web application on your maschine.  You can do it manually or use a Docker. Either require pulling source code from this repository:
```
git clone https://github.com/Vixroff/social-music-app.git
```
and getting personal Musixmatch API KEY from here: https://developer.musixmatch.com/

### **Manually** ###

This way suggests you to set up environment with dependencies by yourself.<br> 
1. Your maschine needs to have installed:
    - Python 3.9^
    - MySQL Server 

2. Create virtual environment and install dependencies:
    ```
    python3 -m venv env
    source env/bin/activate
    pip install requirements.txt
    ```
3. Create ".env" file and define next personal variables:

    | name | value | description |
    | :---- | :----- | :----------- |
    | SECRET_KEY | <'your-secret-key'> | Define any secret key you want. it is needed to secure app. |
    |MUSIXMATCH_API| <'your_api_key'> | Your personal api key to interact with musixmatch serice |
    | DB_USER | <'your-username'> | MySQL profile username |
    | DB_PASSWORD | <'your-password'> | MySQL profile password |
    | DB_NAME | <'db-name'> | Name of database |
    | DB_HOST | **'localhost'** | **!!Constant value**<br> |
    | DB_PORT | <'port-value'> | !!Not-requiered.<br> Default=3306.<br>Define it only when your MySQL server working at the not default port value.

4. Create database with following command
    ```
    python -m db
    ```
    **!! Be sure your MySQL server is enabled.** 

5. Execute migrations
    ```
    python manage.py migrate
    ```
It's enough to complete manual building process on your maschine. To run application enter `make run` command and go to http://127.0.0.1:8000.

### **Docker** ###
This way allows you to create independent network between application and database as isolated containers.<br>
**Installed Docker is requiered.**
1. Create ".env" file and add following variables
    | name | value | description |
    | :---- | :----- | :----------- |
    | SECRET_KEY | <'your-secret-key'> | Define any secret key you want. it is needed to secure app. |
    |MUSIXMATCH_API| <'your_api_key'> | Your personal api key to interact with musixmatch serice |
    | DB_USER | <'your-username'> | MySQL profile username |
    | DB_PASSWORD | <'your-password'> | MySQL profile password |
    | DB_NAME | <'db-name'> | Name of database |
    | DB_HOST | **'mysql'** | **!!Constant value**<br> |
    | DB_CONTAINER_PORT | <'port-value'> | !!Not-requiered.<br> Default=33060.<br>Define it only when you want to use a special port for database container. |

2. Build images and run application:
    ```
    docker-compose -p social-music-app up -d --build
    ```
    **!!Be sure your Docker daemon is enabled.**

Going through these steps automatically builds web service as system of application code and database in isolated environments (containers) and run it on your maschine. 
When it's done go to http://127.0.0.1:8000.
