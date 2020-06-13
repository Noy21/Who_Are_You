import os
import change_all_photos
from flask import Flask, render_template, request
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'uploads'),
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
)

dropzone = Dropzone(app)
PATH_CHANGED = "images/uploads_changed"
PATH_UPLOAD = "uploads"
COMPARE_NAME = "compare"


def split_to_2_lists(a_list):
    """
    splits a list to 2 lists
    :param a_list: the lists we want to split
    :return: two lists.
    """
    mid = len(a_list)//2
    return a_list[:mid], a_list[mid:]


def get_images_lists():
    """
    calls change_all() and split the returned list if needed
    :return: the 2 lists
    """
    list_compares = change_all_photos.ChangeAllPhotos(COMPARE_NAME).change_all()
    if len(list_compares) > 1:
        return split_to_2_lists(list_compares)
    return list_compares, []


@app.route('/', methods=['POST', 'GET'])
def upload():
    """
    handles the index html and the upload
    :return: the index html page
    """
    app.config.update(DROPZONE_MAX_FILES=10)
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')


@app.route('/compare', methods=['POST', 'GET'])
def upload_compare():
    """
    handles the compare html and the upload
    :return: the compare html page
    """
    app.config.update(DROPZONE_MAX_FILES=1)
    if request.method == 'POST':
        f = request.files.get('file')
        extension = os.path.splitext(f.filename)[1]
        f.save(os.path.join(app.config['UPLOADED_PATH'], "compare" + extension))
    return render_template('compare.html')


@app.route('/result')
def result():
    """
    handles the result html
    :return: the result html page
    """
    images = get_images_lists()
    print(images)
    return render_template('result.html', **{'images': images})


if __name__ == '__main__':
    app.run(debug=True)
