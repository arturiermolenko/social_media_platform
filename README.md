## Social Media

### The applications have the following database structure:
![ScreenShot](/schema.jpg)


## Installing / Getting started

A quick introduction of the minimal setup you need to get Social Media app up &
running. With this You will run server with clean Database.

### Python3 must be already installed!

### You also need to install PostgreSQL and create a database.

```shell
git clone https://github.com/arturiermolenko/social_media_platform
cd social_media_platform
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
touch .env
python manage.py migrate
python manage.py runserver
```
Instead of "touch .env" use, please, command "echo > .env" for Windows.
Fill .env file in according to .env_sample

## Running with Docker

Docker must be already installed!

```shell
git clone https://github.com/arturiermolenko/social_media_platform
docker-compose up --build
```

## Features:
- JWT authenticated:
- Admin panel: /admin/
- Documentation is located at: </api/doc/swagger/>, </api/doc/redoc/>
- Create users and posts
- Add comments to posts
- Follow/Unfollow users
- Like/Unlike posts and comments


## Getting access
You can create superuser with :
```shell
python manage.py createsuperuser
```
or create a default user using api/user/register/

To work with token use:

- get access token and refresh token http://127.0.0.1:8000/api/user/token/
- refresh access token http://127.0.0.1:8000/api/user/token/refresh/
- verify access token http://127.0.0.1:8000/api/user/token/verify/

Note: Make sure to send Token in api urls in Headers as follows:

- key: Authorization
- value: Bearer @token


Social media API allows:
- using api/admin/ --- Work with admin panel
- using /api/doc/swagger/ --- Detail api documentation by swagger
- using /api/doc/redoc/ --- Detail api documentation by redoc
- using [POST] /api/user/register/ --- Register a new user
- using [POST] /api/user/token/ --- Obtain new Access and Refresh tokens using credential
- using [POST] /api/user/token/refresh/ --- Obtain new Access token using refresh token
- using [POST] /api/user/token/verify/ --- Verify Access token
- using [GET] /api/user/{id}/ --- Detail user info
- using [PUT, PATCH, DELETE] /api/user/{id}/ --- Update/Delete user(for account owners only)
- using [GET] /api/user/{id}/followers/ --- User's followers
- using [GET] /api/user/{id}/following/ --- Users, that user is following
- using [GET] /api/user/{id}/liked_posts/ --- Posts, that user likes
- using [POST] /api/user/{id}/follow_unfollow/ --- Follow/Unfollow user
######
- using [GET] /api/posts/ --- Posts list
- using [POST] /api/posts/create/ --- Add new post
- using [GET] /api/posts/{post_id}/ --- Detailed post info
- using [POST] /api/posts/{post_id}/ --- Update/Delete post
- using [POST] /api/posts/{post_id}/like_unlike/ --- Like/Unlike post
- using [GET] /api/posts/{post_id}/comments/ --- Post's comments list
- using [POST] /api/posts/{post_id}/comments/add/ --- Add new comment to the post
- using [GET] /api/posts/{post_id}/comments/{id}/ --- Detail info about comment
- using [POST] /api/posts/{post_id}/comments/{id}/ --- Update/Delete comment
- using [POST] /api/posts/{post_id}/comments/{id}/like_unlike/ --- Like/Unlike the comment
