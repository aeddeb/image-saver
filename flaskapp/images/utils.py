from flask import current_app
import secrets
import os
from flask_login import current_user
from flaskapp import db
from flaskapp.models import User, Image
import boto3



def save_image(form_image):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image.filename)
    image_fn = random_hex + f_ext
    image_path = os.path.join(current_app.root_path, 'tmp_images', image_fn)
    form_image.save(image_path)

    return image_fn


def upload_to_s3(image_name):
    access_key = current_app.config['AWS_ACCESS_KEY']
    secret_key = current_app.config['AWS_SECRET_KEY']
    bucket_name = current_app.config['AWS_BUCKET_NAME']

    s3 = boto3.client('s3',
                    aws_access_key_id = access_key,
                    aws_secret_access_key = secret_key)

    local_file = os.path.join(current_app.root_path, 'tmp_images', image_name)
    s3_file = image_name

    s3.upload_file(local_file, bucket_name, s3_file)

    url = f"https://{bucket_name}.s3.amazonaws.com/{s3_file}"

    return url


def delete_from_s3(image_key):
    
    access_key = current_app.config['AWS_ACCESS_KEY']
    secret_key = current_app.config['AWS_SECRET_KEY']
    bucket_name = current_app.config['AWS_BUCKET_NAME']
    
    s3 = boto3.client('s3',
                    aws_access_key_id = access_key,
                    aws_secret_access_key = secret_key)

    s3.delete_object(Bucket=bucket_name, Key=image_key)
