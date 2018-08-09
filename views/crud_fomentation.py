"""
Routes and views for fomentation CRUD.
"""

import json
import os
import re
import glob
import sys
import requests

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import ResearchGroupFactory

from settings.extensions import ExtensionsManager
from werkzeug.utils import secure_filename

from views.forms.content import InstitutionsWithCovenantsForm, EditInstitutionsWithCovenantsForm 

from bson.json_util import dumps

crud_fomentation = Blueprint('crud_fomentation', __name__, url_prefix='/admin')

@crud_fomentation.route('/add_fomentos/', methods=['GET', 'POST'])
@login_required
def add_fomentation():
    """Render fomentation adding form."""

    allowed_extensions = ['jpg', 'png']

    form = InstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()

    if form.validate_on_submit() and form.create.data:
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets/fomentation")
            filename = secure_filename(photo.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'crud_fomentation.add_fomentation',
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            uploadFiles(photo, path, logoFile)
            new_fomentation = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'logoFile': logoFile,
                'description': form.description.data
            }

        dao.find_one_and_update(None, {
            '$push': {'fomentation' : new_fomentation}
        })

        return redirect(
            url_for(
                'crud_fomentation.add_fomentation',
                success_msg='Fomento adicionado com sucesso.',
            )
        )


    return render_template(
        'admin/add_fomentation.html',
        form=form,
        success_msg=request.args.get('success_msg'),
    )

@crud_fomentation.route('/deletar_fomentos/', methods=['GET', 'POST'])
@login_required
def delete_fomentation():
    """Render fomentation deleting form."""

    form = EditInstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    integrations = pfactory.integrations_infos_dao().find_one()
    integrations = dict(integrations)
    integrations = dumps(integrations)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'fomentation.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'crud_fomentation.delete_fomentation',
                success_msg='Fomento deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_fomentation.html',
        form=form,
        integrations=integrations,
        success_msg=request.args.get('success_msg')
    )

@crud_fomentation.route('/editar_fomentos/', methods=['GET', 'POST'])
@login_required
def edit_fomentation():
    """Render fomentation editing form."""

    allowed_extensions = ['jpg', 'png']

    form = EditInstitutionsWithCovenantsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    integrations = pfactory.integrations_infos_dao().find_one()
    integrations = dict(integrations)
    integrations = dumps(integrations)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        if form.logo.data and allowedFile(form.logo.data.filename, allowed_extensions):
            photo = form.logo.data
            path = os.path.normpath("static/assets/fomentation")
            filename = secure_filename(photo.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'crud_fomentation.edit_fomentation',
                        success_msg='Nome da logo contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            logoFile = 'logo-' + form.initials.data.lower() + '.' + extension
            logo = uploadFiles(photo, path, logoFile)
            new_fomentation = {
                'name': form.name.data,
                'initials': form.initials.data.upper(),
                'description': form.description.data,
                'logoFile': logo
            }

            dao.find_one_and_update(None, {
                '$set': {'fomentation.' + index : new_fomentation}
            })
        else:
            dao.find_one_and_update(None, {
                '$set': {'fomentation.' + index + '.description' : form.description.data}
            })
            dao.find_one_and_update(None, {
                '$set': {'fomentation.' + index + '.initials' : form.initials.data.upper()}
            })
            dao.find_one_and_update(None, {
                '$set': {'fomentation.' + index + '.name' : form.name.data}
            })

        return redirect(
            url_for(
                'crud_fomentation.edit_fomentation',
                success_msg='Fomento editado com sucesso.'
            )
        )


    return render_template(
        'admin/edit_fomentation.html',
        form=form,
        integrations=integrations,
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

