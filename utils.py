import os
from werkzeug.utils import secure_filename


def save_img(data, path):
    f = data
    filename = secure_filename(f.filename)
    try:
        os.mkdir(path)
    except:
        pass
    f.save(os.path.join(path, filename))