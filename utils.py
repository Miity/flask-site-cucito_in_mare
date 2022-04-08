import os
from werkzeug.utils import secure_filename


def save_img(data, path, filename=None):
    f = data
    if filename is None:
        filename = secure_filename(f.filename)
    else:
        secure_filename(f.filename)
        f.filename = filename
        filename = f.filename
    try:
        os.mkdir(path)
    except:
        pass
    f.save(os.path.join(path, filename))
