"""
Routes and views for system administration pages.
"""
import os
import re
import glob
import sys

from flask_login import LoginManager, \
    login_user, login_required, logout_user, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from bson.objectid import ObjectId

from werkzeug.utils import secure_filename

from models.factory import ResearchGroupFactory
from models.users import User

from settings.extensions import ExtensionsManager

from views.forms.auth import LoginForm
from views.forms.content import ParticipationsInEventsForm, \
    ScheduledReportForm, InstitutionsWithCovenantsForm, \
    DocumentForm, SubjectsForm, ProfessorForm, StaffForm, CalendarForm, \
    EditInstitutionsWithCovenantsForm, EditDocumentForm

from bson.json_util import dumps
import json
import requests

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
##############################################################################
#Adicionar deletar e editar convênios(Não finalizado)
###############################################################################

@APP.route('/convenios/', methods=['GET', 'POST'])
@login_required
def covenants():
    """Render covenant adding form."""

    allowed_extensions = ['jpg', 'png']

    form = InstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()

    if form.validate_on_submit() and form.create.data:
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets")
            filename = secure_filename(photo.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'admin.covenants',
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            uploadFiles(photo, path, logoFile)
            new_covenant = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'logoFile': logoFile
            }

        dao.find_one_and_update(None, {
            '$push': {'institutionsWithCovenant': new_covenant}
        })

        return redirect(
            url_for(
                'admin.covenants',
                success_msg='Convênio adicionado adicionado com sucesso.'
            )
        )


    return render_template(
        'admin/covenants.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/deletar_convenios/', methods=['GET', 'POST'])
@login_required
def delete_covenants():
    """Render covenant deleting form."""

    form = EditInstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'institutionsWithCovenant.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'admin.delete_covenants',
                integrations=json,
                success_msg='Convênio deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_covenants.html',
        form=form,
        integrations=json,
        success_msg=request.args.get('success_msg')
    )

@APP.route('/editar_convenios/', methods=['GET', 'POST'])
@login_required
def edit_covenants():
    """Render covenant editing form."""

    allowed_extensions = ['jpg', 'png']

    form = EditInstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets")
            filename = secure_filename(photo.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'admin.edit_covenants',
                        integrations=json,
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            uploadFiles(photo, path, logoFile)
            new_covenant = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'logoFile': logoFile
            }

            dao.find_one_and_update(None, {
                '$set': {'institutionsWithCovenant.' + index : new_covenant}
            })
        else:
            new_covenant = {
                'name': form.name.data,
                'initials':form.initials.data.upper()
            }

            dao.find_one_and_update(None, {
                '$set' : {'institutionsWithCovenant.' + index : new_covenant}
            })

        return redirect(
            url_for(
                'admin.edit_covenants',
                integrations=json,
                success_msg='Convênio editado com sucesso.'
            )
        )


    return render_template(
        'admin/edit_covenants.html',
        form=form,
        integrations=json,
        success_msg=request.args.get('success_msg')
    )

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
