# social-music-app #

## **Description** ##

### **About** ###
This is my playground — a web application based on Django Framework and represents a social network focused on music content. A platform suggests users to interact with "MusixMatch" musics library, collect favorite tracks and create personal playlists, share them with a friends, like and discuss it.

**"Personal music playlist is a kind of personality reflection"** - sense of these words inspired me to start working on this project that general idea is taking main features from applications like: "Instagram", "Facebook" and applying them in my app with focusing to musical context. Quite like "Spotify" i guess with extras.

### **Tech specification** ###
"social-music-app" provides many user's capabilities:

- Profiles. Create a personal profile by passing registration form and collect any content there.
- Content manager. Add or remove any type of content from your profile.
- Searching. Find any track or artist by name, also users profile.
- Followings. Follow or unfollow users who are your friends or just have a good music taste, inspect their profiles to see all content they have.
- Recommendations. Get personal profiles recommendations for you.
- Trends. MusixMatch API allows to be with worldwide musics trends. Just get the most streamed content.
- Creating playlists. Create playlists with special music.
- Discuss. If you want tell something about playlist you are able to do that leaving a comment.

Project is currently raw but work doesn't stop on it. There are many things to impove/fix/

---
## **Build** ##
There are several ways to build web application on your maschine.  You can do it manually or use a Docker. Either require pulling source code from this repository:
```
git clone https://github.com/Vixroff/social-music-app.git
```
and getting personal Musixmatch API KEY from [here](https://developer.musixmatch.com/)
<br>
<br>

### **Manually** ###
This way suggests you to start application at your maschine without network isolation.

Check that your maschine has installed:
- Python 3.9
- MySQL Server
- Poetry

Create ".env" file at root directory and define next personal variables:
| name | value | description |
| :---- | :----- | :----------- |
| SECRET_KEY | "<your-secret-key\>" | Secret key of application. It is needed to secure app. |
|MUSIXMATCH_API| "<your_api_key\>" | API key of musixmatch service |
| DB_USER | "<your-username\>" | MySQL profile username |
| DB_PASSWORD | "<your-password\>" | MySQL profile password |
| DB_NAME | "<db-name\>" | Database scheme name |
| DB_HOST | **"localhost"** | **Constant value** |
| DB_PORT | "<port-value\>" |  Default=3306.<br>MySQL server port |

Create database with following command
```
python -m db
```
**!! Be sure your MySQL server is enabled.** 

Execute migrations and run server.
```
make migrate
make run
```
And its done!! Go to http://127.0.0.1:8000 and use it.
<br>
<br>

### **Docker** ###
This way allows you to create independent network between application and database as isolated containers.<br>
**!! Installed Docker is requiered.**

Create ".env" file and add following variables
| name | value | description |
| :---- | :----- | :----------- |
| SECRET_KEY | "<your-secret-key\>" | Secret key of application. It is needed to secure app. |
|MUSIXMATCH_API| "<your_api_key\>" | API key of musixmatch service |
| DB_USER | "<your-username\>" | MySQL profile username |
| DB_PASSWORD | "<your-password\>" | MySQL profile password |
| DB_NAME | "<db-name\>" | Database scheme name |
| DB_HOST | **"mysql"** | **Constant value**<br> |
| DB_CONTAINER_PORT | "<port-value\>" | Default=33060.<br>Database container port |

Build images and run application:
```
docker-compose -p social-music-app up -d --build
```
**!!! Be sure your Docker daemon is enabled.**


Going through these steps automatically builds web service as system of application code and database in isolated environments (containers) and run it on your maschine. 
When it's done go to http://127.0.0.1:8000.

---
