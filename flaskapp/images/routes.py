from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint,
                   current_app)
from flask_login import current_user, login_required
from flaskapp import db
from flaskapp.models import Image
from flaskapp.images.forms import UploadImageForm
from flaskapp.images.utils import save_image, upload_to_s3, delete_from_s3
import os

images_bp = Blueprint('images', __name__)

@images_bp.route("/upload", methods = ['GET', 'POST'])
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
        tmp_file = os.path.join(current_app.root_path, 'user_images', image_file)
        os.remove(tmp_file)
        flash('Upload Successful.', 'success')
        return redirect(url_for('images.images'))
    return render_template('upload.html', title='Upload an Image', form=form)

@images_bp.route("/images", methods = ['GET', 'POST'])
@login_required
def images():
    if current_user.is_authenticated:
        user_id = current_user.id
        images = Image.query.filter_by(user_id=user_id).all()
    return render_template('images.html', title='Images' , images=images)


@images_bp.route("/image/<int:image_id>")
@login_required
def image(image_id):
    if current_user.is_authenticated:
        user_id = current_user.id
        image_obj = Image.query.filter_by(user_id=user_id, id=image_id).first()
        if image_obj:
            image = Image.query.get_or_404(image_id)

    return render_template('image.html', title=image.title, image=image)


@images_bp.route("/image/<int:image_id>/delete", methods = ['POST'])
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
    return redirect(url_for('images.images'))