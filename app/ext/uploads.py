from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

def configure(app):
    photos = UploadSet('photos', IMAGES)
    configure_uploads(app, photos)
    patch_request_class(app)
