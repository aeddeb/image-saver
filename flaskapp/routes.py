from flask import render_template, url_for, flash, redirect, request
from flaskapp import app, db, bcrypt, mail
from flaskapp.forms import (RegistrationForm, LoginForm, UpdateAccountForm, UploadImageForm, 
                            RequestResetForm, ResetPasswordForm)
from flaskapp.models import User, Image
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.upload import save_image, upload_to_s3, delete_from_s3
from flask_mail import Message
import os


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You can now log in.", 'success') # Second arg is bootstrap class
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/upload", methods = ['GET', 'POST'])
@login_required
def upload():
    form = UploadImageForm()
    if form.validate_on_submit():
        image_file = save_image(form.image.data)
        # save to s3
        s3_url = upload_to_s3(image_file)
        # add to db
        image = Image(title=image_file, s3_path=s3_url, poster=current_user)
        db.session.add(image)
        db.session.commit()
        # delete it form the temp storage
        tmp_file = os.path.join(app.root_path, 'user_images', image_file)
        os.remove(tmp_file)
        flash('Upload Successful.', 'success')
        return redirect(url_for('images'))
    return render_template('upload.html', title='Upload an Image', form=form)

@app.route("/images", methods = ['GET', 'POST'])
@login_required
def images():
    if current_user.is_authenticated:
        user_id = current_user.id
        images = Image.query.filter_by(user_id=user_id).all()
    return render_template('images.html', title='Images' , images=images)


@app.route("/image/<int:image_id>")
@login_required
def image(image_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        image_obj = Image.query.filter_by(user_id=user_id, id=image_id).first()
        if image_obj:
            image = Image.query.get_or_404(image_id)

    return render_template('image.html', title=image.title, image=image)


@app.route("/image/<int:image_id>/delete", methods = ['POST'])
@login_required
def delete_image(image_id):
    image = Image.query.get_or_404(image_id)
    if image.poster != current_user:
        abort(403)
    # Delete from s3
    delete_from_s3(image.title)
    # Delete from db
    db.session.delete(image)
    db.session.commit()
    flash('Your image has been deleted.', 'success')
    return redirect(url_for('images'))

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', 
                    sender = app.config['MAIL_USERNAME'],
                    recipients = [user.email])
    msg.body = f"""To reset your password, please visit the following link:
{url_for('reset_token', token=token, _external=True)}

If you did not make this request, please ignore this email and no changes will be made.
"""
    mail.send(msg)

@app.route("/reset_password", methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("If an account with this email address exists, a password reset email will be sent shortly.", 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been updated! You can now log in.", 'success') # Second arg is bootstrap class
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)