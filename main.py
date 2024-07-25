from flask import Flask, render_template, send_from_directory, url_for
from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField
import numpy as np
from PIL import Image
import operator

app = Flask(__name__)
app.config['SECRET_KEY'] = '8383kkke8ed8w8092kd82eksah'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/uploads/<filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)


class UploadForm(FlaskForm):
    photo = FileField(validators=[FileAllowed(photos, "Only images are allowed"),
                                        FileRequired('File field should not be empty')])
    submit = SubmitField('Upload')


def analyze_img(img_path):
    image = Image.open(img_path[1:])
    img = np.array(image)
    colors = {}
    for a_list in img:
        for an_array in a_list:
            try:
                colors[tuple(an_array)] += 1
            except KeyError:
                colors[tuple(an_array)] = 1
    sorted_colors = sorted(colors.items(), key=operator.itemgetter(1), reverse=True)
    top_ten = sorted_colors[0:10]
    return top_ten


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    form = UploadForm()
    top_10 = []
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_file', filename=filename)
        top_10 = analyze_img(file_url)
    else:
        file_url = None
    return render_template('index.html', form=form, file_url=file_url, data=top_10)


if __name__ == '__main__':
    app.run(debug=True)


