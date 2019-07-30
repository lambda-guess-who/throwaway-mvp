
# Guess Who Flask/React MVP

Sample flask Docker Compose project with heroku deployment configuration

## Getting started

### Local Development
### 0. Create `.env` file
create the the`.env` file at the root directory. copy the `dotenvsample` file and assign values
```
#Twitter API key ( https://developer.twitter.com/)
TWITTER_CONSUMER_KEY=
TWITTER_CONSUMER_SECRET=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
# Basilica https://www.basilica.ai/api-keys/
BASILICA_KEY=
# Secret key for signing json web tokens generate a long random string `openssl rand -base64 40` should be fine.
# You can put anything here for dev but please generate a secure random string when deploying
HS256_KEY=
```

### 1. Build the image:

```console

$ docker-compose build

```

### 2. Initialize the Database

[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are used to manage db schema and migrations.

```console

$ docker-compose run web_app flask db upgrade

```

The command may fail on the first try if the database container is slow to boot up. If it failed, simply rerun the command again.

Alternatively you can use this command instead:

```console

$ docker-compose run web_app ./wait-for-pg.sh db flask

```

### 3. Start the dev server

```console

$ docker-compose up

```

This will run the flask development web server for `backend` and the react dev server for `frontend`

The default runs on port 3000 by default for development. Open `localhost:3000` on the browser to view the app.

You can now start adding code to `backend` (flask) or `frontend` (react). The flask and react development web servers are configure to reload on code change.

  

Hit `CTRL-C` to exit.

  

### 4a. Installing additional packages (backend)

Uses `pyenv` to manage depency versions but not for virtual environments.

```console

$ docker-compose run backend pyenv install [package]

```

We still need to rebuild the image if we installed a dependency:

```console

$ docker-compose build

```

  

### 4b. Installing additional packages (frontend)

Uses `npm` to install packages

```console

$ docker-compose run frontend npm install [package]

```

We still need to rebuild the image if we installed a dependency:

```console

$ docker-compose build

```

  

## Deploying to Heroku:

### 1. Setup Heroku-CLI

See official Docs: https://devcenter.heroku.com/articles/heroku-cli

### 2. Commit your changes to Git:

If you did not clone this repo, make sure to have git initialized on the root directory (where `heroku.yml` lives).

Commit your changes to Git.

```

$ git add .

$ git commit -m "Commit message"

```

### 3. Create the heroku app and deploy:

Upgrade to heroku-cli beta and install plugin-manifest

```console

$ heroku update beta

$ heroku plugins:install @heroku-cli/plugin-manifest

```

Create the heroku app

```console

$ heroku create [your-app-name] --manifest

```
Add the environmental variables value from the `.env` file to your project settings.

Deploy the app via git

```console

$ git push heroku master

```

This will rebuild the docker image and deploy it to heroku. It may take while to complete the rebuild.

  

### Open your Web App in the browser:

```

$ heroku open

```