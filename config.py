class Configuration(object):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://mare_admin:qazzaq@localhost/mare_db'
    SECRET_KEY = 'qazzaq'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
      

    ### Flask security
    SECURITY_PASSWORD_SALT = 'solt'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    ### upload set
    UPLOAD_FOLDER = 'static/upload/'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
    MAX_CONTENT_LENGTH = 16 * 1000 * 1000

    
    ### CKEDITOR 
    #CKEDITOR_PKG_TYPE = 'basic'
    CKEDITOR_FILE_UPLOADER = 'upload'



