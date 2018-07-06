"""Flask extensions configuration."""

from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS


class ExtensionsManager:
    """An app's Flask extensions manager."""
    csrf = CSRFProtect()
    login_manager = LoginManager()

    def __init__(self):
        """This will raise an exception."""
        raise NotImplementedError('Use only static members for this class.')

    @staticmethod
    def auto_configure(app):
        """Initialize extensions needed for this Flask app."""
        app.config['SECRET_KEY'] = 'english,motherfucker!doyouspeak?'
        app.config['WTF_CSRF_FIELD_NAME'] = 'csrf_token'

        ExtensionsManager.csrf.init_app(app)
        ExtensionsManager.login_manager.init_app(app)
        CORS(app, supports_credentials=True)
