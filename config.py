class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///myblog.db'
    SECRET_KEY = 'qazzaq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_FILE_UPLOADER = 'upload'
      

    ### Flask security
    SECURITY_PASSWORD_SALT = 'solt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'