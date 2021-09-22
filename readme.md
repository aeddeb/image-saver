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

```bash
# clone the repository
$ git clone https://github.com/aeddeb/image-saver
$ cd image-saver
```

Create a virtualenv, activate it and install the requirements:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Setup and Configuration
Before running the application, there are a few things that need to be set up.
### AWS
You need to create an AWS s3 bucket to save images uploaded by users. The s3 bucket needs to be set to publically accessible with read access. <i>Please note that setting public access to a s3 bucket is not recommended by Amazon as any anonymous user can read objects from the bucket.</i> 

You will need to then export 3 environment variables: AWS_ACCESS_KEY, AWS_SECRET_KEY, AWS_BUCKET_NAME.
```bash
$ export AWS_ACCESS_KEY="type your access key"
$ export AWS_SECRET_KEY="type your secret key"
$ export AWS_BUCKET_NAME="type you bucket name"
```
It is recommended to export these 3 environment variables within the .bash_profile (or .bashrc) file, which is located in your home directory, rather than entering the sensitive info within the terminal.

### Configuration

You will need to export additional environment variables. These are:
1. SECRET_KEY - a secret key needed for CSRF protection. This can be a random string.
2. EMAIL_USER - an email that your app will use to send emails to user when they request a password reset. Please you a googlemail (gmail) account. If not, you will need to change the SMTP service which can be found in flaskapp/config.py (the variable is MAIL_SERVER).
3. EMAIL_PASS - the password for the email
4. SQLALCHEMY_DATABASE_URI - the URI for the sqlite database. You can use "sqlite:///site.db"

```bash
$ export SECRET_KEY="your secret key"
$ export EMAIL_USER="email@example.com"
$ export EMAIL_PASS="password"
$ export SQLALCHEMY_DATABASE_URI="sqlite:///site.db" 
```

Just like for the AWS environment variables, it is recommended to export these environment variables within the .bash_profile (or .bashrc) file.

<i>Note: please restart your terminal once you have saved all the export commands in the .bash_profile (or .bashrc) file.</i>

### Database
In order to initialize the sqlite database, run:
```bash
$ python3 setup_db.py
```

## Run App
To run the application, export a FLASK_APP environment variable as the flask application and then use the flask run command. Additionally, if you would like to run in development mode, you have to set FLASK_ENV to development.

```bash
$ export FLASK_APP=flaskapp
$ export FLASK_ENV=development
$ flask run
```
Once running, the app is hosted on: http://127.0.0.1:5000/

## Testing
Tests were generated using the pytest library. To run the tests, run the following command in the terminal:
```bash
$ pytest
```

Currently there is only one example test for demonstration purposes. I ran into some issues with setting up a temporary database within the testing context of the app. Once this is resolved, I would like to add a comprehensive suite of tests to test functionality such as registrations, logins, image uploads and so on.


## Credits
I followed a great [tutorial series by Corey Schafer](https://www.youtube.com/watch?v=MwZwr5Tvyxo&list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH&ab_channel=CoreySchafer) on how to build a flask app. [Click here](https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog) to view his github repo.
