# Image Saver App

This web app allows you to create a service for users to register an account, login and upload images into a personal repository.

## Design
- The web app is built using the Flask web app framework
- A sqlite database is used for the purpose of the demo
    - The database stores Users and their Images
    - The Image files are not directly stored in the database; the images are stored in an AWS s3 bucket and their s3 URL is stored in the database
- Once registered and logged in, a user:
    - Can save an image into their personal gallery which is uploaded to an AWS s3 bucket.
    - Can view all their saved images in the /images page. Images are served from s3 by retrieving all s3 URLs from the database connected to the user.
    - Can download or delete an image. Deleted images are removed from s3 and the database.

## Installation

```
# clone the repository
$ git clone https://github.com/aeddeb/image-saver
$ cd image-saver
$ cd examples/tutorial
```

Create a virtualenv, activate it and install the requirements:

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Setup
Before running the application, there are a few things that need to be set up.
### AWS
You need to create an AWS s3 bucket to save images uploaded by users. The s3 bucket needs to be set to publically accessible with read access. <i>Please note that setting public access to a s3 bucket is not recommended by Amazon as any anonymous user can read objects from the bucket.</i> I would recommend looking into improving security and access to the s3 bucket.

You will need to then export 3 environment variables: AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME.
```
$ export AWS_ACCESS_KEY="type your access key"
$ export AWS_SECRET_KEY="type your secret key"
$ export AWS_BUCKET_NAME="type you bucket name"
```
It is recommended to export these 3 environment variables within the .bash_profile (or .bashrc) file rather than entering the sensitive info within the terminal.

### Database
In order to initialize the sqlite database, run:
```
$ python3 setup_db.py
```

## Run App
To run the application, export a FLASK_APP environment variable as the flask application and then use the flask run command. Additionally, flask defaults to run in production mode. If you would like to run in development mode, you have to set FLASK_env to development.

```
$ export FLASK_APP=flaskapp
$ export FLASK_ENV=development
$ flask run
```

## Testing
Tests were generated using the pytest library. To run the tests, run the following in the terminal:
```
$ pytest
```

Currently there is only one example test for demonstration purposes. I ran into some issues with setting up the database within the testing context of the app. Once this is resolved, I would like to add a comprehensive suite of tests to test functionality such as registrations, logins, image uploads and so on.


## Credits
I followed a great tutorial series by Corey Schafer on how to build a flask app. [Click here](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog) to view his github repo.
