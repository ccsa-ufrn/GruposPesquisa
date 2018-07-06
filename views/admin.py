"""
Routes and views for system administration pages.
"""
import os
import re
import glob
import sys

from flask_login import LoginManager, \
    login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request, current_app

from flask_mail import Message, Mail

from bcrypt import hashpw, gensalt

from bson.objectid import ObjectId

from werkzeug.utils import secure_filename

from models.factory import ResearchGroupFactory
from models.users import User

from settings.extensions import ExtensionsManager

from views.forms.auth import LoginForm, NickForm, ResetPasswordForm
from views.forms.content import DocumentForm, EditDocumentForm

from bson.json_util import dumps
import json
import requests
import random
import string

import datetime

APP = Blueprint('admin',
                __name__,
                static_folder='static',
                url_prefix='/admin')


@APP.route('/')
def index():
    """
    If user is already authenticated, render its
    dashboard, otherwise ask for his password.
    """
    if current_user and current_user.is_authenticated:

        pfactory = ResearchGroupFactory(current_user.group_name)
        research_group = pfactory.research_group

        return render_template(
            'admin/index.html',
            research_group=research_group
        )

    else:
        return login()


@APP.route('/login/', methods=['GET', 'POST'])
def login():
    """
    Render an user authorization form.
    """
    form = LoginForm()

    if form.validate_on_submit():
        user_attempting = User.get(form.nick.data)

        if (user_attempting is not None) and (user_attempting.authenticate(form.password.data)):
            login_user(user_attempting)
            return index()
        else:
            return render_template(
                'admin/login.html',
                form=form,
                incorrect_attempt=True
            )
    else:
        return render_template(
            'admin/login.html',
            form=form,
            incorrect_attempt=False
        )


@APP.route('/logout/')
@login_required
def logout():
    """
    Render a logged out page.
    """

    logout_user()

    return render_template(
        'admin/logout.html'
    )

@APP.route('/solicitar_email/', methods=['GET','POST']) 
def request_email():
    """
    Render a form for the user to ask for a password reset link 
    """
    form = NickForm()
    pfactory = ResearchGroupFactory()
    dao = pfactory.reset_keys_dao()

    if form.validate_on_submit():
        user_requesting = User.get(form.nick.data)
        if user_requesting is not None:
            user_mail = user_requesting._email
            user_group = user_requesting._group_name
            key = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
            expires_in = datetime.datetime.now() + datetime.timedelta(hours=1)
            new_key = {
                'key': key,
                'email': user_mail,
                'expiresIn': expires_in,
                'groupName': user_group
            }
            dao.insert_one(None, new_key)
            mail = Mail(current_app)
            msg = Message('Teste', 
                    sender='assessoriatecnica@ccsa.ufrn.br',
                    recipients=['luccasmmg@gmail.com'])
            msg.body = 'localhost:3001/admin/mudar_password/?key=' + key
            mail.send(msg)
            return redirect(
                url_for(
                'admin.request_email'
                )
            )
        else:
            return redirect(
                url_for(
                'admin.request_email',
                incorrect_attempt=True
                )
            )
    return render_template(
        'admin/request_email.html',
        form=form
    )

@APP.route('/mudar_password/', methods=['GET', 'POST'])
def change_password():
    """
    Render a form for changing password
    """
    key = request.args.get('key')
    form = ResetPasswordForm(key=key)
    pfactory = ResearchGroupFactory()
    dao = pfactory.reset_keys_dao()
    user_dao = pfactory.research_groups_dao()
    if form.validate_on_submit() and form.password_one.data == form.password_two.data:
        reset_document = dict(dao.find_one({'key': form.key.data}))
        if reset_document['expiresIn'] > datetime.datetime.now():
            password_one = hashpw(form.password_one.data.encode('utf-8'), gensalt(14))
            password_one = password_one.decode('utf-8')
            user_dao.find_one_and_update({'name': reset_document['groupName']},{
                '$set' : {'users.0.password': password_one}
            })
        return redirect(
            url_for(
                'admin.login'
            )
        )
    return render_template(
        'admin/reset_password.html',
        form=form,
        key=key
    )

@ExtensionsManager.login_manager.user_loader
def user_loader(user_id):
    """Load an user from database,
    using an user_id string formatted like 'user_nick@group_name'."""
    match = re.match('(?P<nick>.*)@(?P<name>.*)', user_id)
    if match is not None:
        return User.get(
            match.group('nick'),
            authenticated=True
        )
    else:
        return None
###############################################################################
#Adicionar deletar e editar documentos
###############################################################################

@APP.route('/documentos/', methods=['GET', 'POST'])
@login_required
def documents():
    """Render document adding form."""

    allowed_extensions = ['docx', 'pdf']

    form = DocumentForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.official_documents_dao()
    ownerProgram = pfactory.mongo_id

    if form.validate_on_submit() and form.create.data:
        insertedOn = datetime.datetime.now()
        insertedBy = current_user._full_name
        document = form.document.data
        path = os.path.normpath("static/upload_files/" + current_user.group_name.lower())
        if allowedFile(document.filename, allowed_extensions):
            filename = uploadFiles(document, path, document.filename)
            new_document = {
                'ownerProgram': ownerProgram,
                'category': form.category.data,
                'title': form.title.data,
                'cod': form.cod.data,
                'file': filename,
                'insertedOn': insertedOn,
                'insertedBy': insertedBy
            }

            dao.insert_one(None, new_document)

            return redirect(
                url_for(
                    'admin.documents',
                    success_msg='Documento adicionado adicionado com sucesso.'
                )
            )
        else:

            return redirect(
                url_for(
                    'admin.documents',
                    success_msg='',
                    invalid_type='Tipo de documento inválido'
                )
            )

    return render_template(
        'admin/documents.html',
        documents=dao.find_one(),
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_documentos/', methods=['GET', 'POST'])
@login_required
def delete_documents():
    """Render document deleting form."""

    form = EditDocumentForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.official_documents_dao()
    json = pfactory.official_documents_dao().find()
    json = list(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
            '$set' : {'deleted' : ''}})
        return redirect(
            url_for(
                'admin.delete_documents',
                success_msg='Documento deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_documents.html',
        documents=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )


@APP.route('/editar_documentos/', methods=['GET', 'POST'])
@login_required
def edit_documents():
    """Render document editing form."""

    allowed_extensions = ['docx', 'pdf']

    form = EditDocumentForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.official_documents_dao()
    ownerProgram = pfactory.mongo_id
    json = pfactory.official_documents_dao().find()
    json = list(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        document_id = form.document_id.data
        if form.document.data:
            if allowedFile(form.document.data.filename, allowed_extensions):
                insertedOn = datetime.datetime.now()
                insertedBy = current_user._full_name
                document = form.document.data
                path = os.path.normpath("static/upload_files/" + current_user.group_name.lower())
                filename = uploadFiles(document, path, document.filename)
                new_document = {
                    'title': form.title.data,
                    'cod': form.cod.data,
                    'file': filename,
                    'insertedBy': insertedBy,
                    'insertedOn': insertedOn
                }

                dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
                    '$set' : new_document
                })
            else:
                return redirect(
                    url_for(
                        'admin.edit_documents',
                        success_msg='Tipo de documento inválido'
                    )
                )

        else:
            new_document = {
                'title':form.title.data,
                'cod': form.cod.data
            }
            dao.find_one_and_update({'_id' : ObjectId(form.document_id.data)}, {
                '$set' : new_document
            })

        return redirect(
            url_for(
                'admin.edit_documents',
                success_msg='Documento editado com sucesso.'
            )
        )

    return render_template(
        'admin/edit_documents.html',
        documents=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )

def uploadFiles(document, path, filename):
    """3 functions, effectively upload files to server,
    if a file with the same name already exists, change filename
    to filename_x and also prevent not secure filenames ex: with / * etc
    """
    name, extension = (secure_filename(filename)).split('.')
    checkpath = os.path.join((os.getcwd()), path, os.path.normpath(name))
    if glob.glob(checkpath + '*.' + extension):
        numberofcopies = 0
        dirs = glob.glob(checkpath + '*.' + extension)
        for i in dirs:
            numberofcopies += 1
        filename = name + '_' + str(numberofcopies) + '_.' + extension
    filename = secure_filename(filename)
    document.save(os.path.join((os.getcwd()), path, os.path.normpath(filename)))
    return filename

def allowedFile(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@APP.route('/401/')
@ExtensionsManager.login_manager.unauthorized_handler
def unauthorized():
    """Render page to be showed up for not logged in users."""
    return render_template('admin/401.html')


@APP.route('/404/')
@APP.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error))
    return render_template('admin/404.html',), 404
