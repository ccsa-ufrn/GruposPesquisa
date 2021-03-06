"""
This script runs the application using a development server.
"""
# import locale

from flask_cors import CORS
from flask import Flask, logging
from models.clients.util import keyring
import os

from views.admin import APP as admin_app
from views.crud_books import crud_books
from views.crud_articles import crud_articles
from views.crud_attendances import crud_attendances
from views.crud_projects import crud_projects
from views.crud_events import crud_events
from views.crud_participations import crud_participations 
from views.crud_staff import crud_staff 
from views.crud_covenants import crud_covenants 
from views.crud_magazines import crud_magazines 
from views.crud_fomentation import crud_fomentation
from views.crud_scheduled_reports import crud_scheduled_reports 
from views.crud_news import crud_news 
from views.avaliation_form import avaliation_form 
from views.public import app as public_app
from settings.extensions import ExtensionsManager

mail_dict = keyring.get(keyring.MAIL)
MAIL_USER = mail_dict['mail_user']
MAIL_PASSWORD = mail_dict['mail_password']

APP = Flask(__name__)
CORS(APP, supports_credentials=True)
APP.config.update(
    TRAP_BAD_REQUEST_ERRORS = True,
    #EMAIL SETTINGS
    MAIL_SERVER='mx5.ufrn.br',
    MAIL_PORT = 465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=MAIL_USER,
    MAIL_PASSWORD=MAIL_PASSWORD
)
APP.debug = True
ExtensionsManager.auto_configure(APP)

APP.register_blueprint(public_app)
APP.register_blueprint(admin_app)
APP.register_blueprint(crud_books)
APP.register_blueprint(crud_articles)
APP.register_blueprint(crud_attendances)
APP.register_blueprint(crud_projects)
APP.register_blueprint(crud_events)
APP.register_blueprint(crud_staff)
APP.register_blueprint(crud_covenants)
APP.register_blueprint(crud_magazines)
APP.register_blueprint(crud_fomentation)
APP.register_blueprint(crud_participations)
APP.register_blueprint(crud_scheduled_reports)
APP.register_blueprint(crud_news)
APP.register_blueprint(avaliation_form)

PUBLIC_HOST = '0.0.0.0'
PUBLIC_PORT = 3002
DEV_HOST = 'localhost'
DEV_PORT = 3002 

if __name__ == '__main__':

    try:
        APP.run(PUBLIC_HOST, PUBLIC_PORT)
    except PermissionError:
        print('DEVELOPMENT MODE: running at localhost only!!!')
        APP.jinja_env.auto_reload = True
        APP.config['TEMPLATES_AUTO_RELOAD'] = True
        APP.run(DEV_HOST, DEV_PORT, debug=True)
