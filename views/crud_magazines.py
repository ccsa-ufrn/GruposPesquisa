"""
Routes and views for add_magazine CRUD.
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

from views.forms.content import MagazinesForm, EditMagazinesForm 

from bson.json_util import dumps

crud_magazines = Blueprint('crud_magazines', __name__, url_prefix='/admin')

##############################################################################
#Adicionar deletar e editar periódicos 
###############################################################################

@crud_magazines.route('/add_periódico/', methods=['GET', 'POST'])
@login_required
def add_magazine():
    """Render covenant adding form."""

    allowed_extensions = ['jpg', 'png']

    form = MagazinesForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.publications_dao()

    if form.validate_on_submit() and form.create.data:
        if form.cover.data and allowedFile(form.cover.data.filename, allowed_extensions):
            cover = form.cover.data
            path = os.path.normpath("static/assets/magazines")
            filename = secure_filename(cover.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'crud_magazines.add_magazine',
                        success_msg='Nome do arquivo com a foto contem mais de um . por favor corriga isso'
                    )
                )
            name, extension = filename.split('.')
            uploadFiles(cover, path, filename)
            new_magazine = {
                'name': form.name.data,
                'coverFile': filename,
                'description': form.description.data,
                'issn' : form.issn.data
            }

        dao.find_one_and_update(None, {
            '$push': {'magazines' : new_magazine}
        })

        return redirect(
            url_for(
                'crud_magazines.add_magazine',
                success_msg='Periódico adicionado com sucesso',
            )
        )


    return render_template(
        'admin/add_magazine.html',
        form=form,
        success_msg=request.args.get('success_msg'),
    )

@crud_magazines.route('/deletar_periodicos/', methods=['GET', 'POST'])
@login_required
def delete_magazine():

    form = EditMagazinesForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.publications_dao()
    magazines = pfactory.publications_dao().find_one()
    magazines = dict(magazines)['magazines']
    magazines = dumps(magazines)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        dao.find_one_and_update(None, {
            '$set': {'magazines.' + index + '.deleted' : ""}
        })
        return redirect(
            url_for(
                'crud_magazines.delete_magazine',
                success_msg='Periódico deletado com sucesso.'
            )
        )

    return render_template(
        'admin/delete_magazine.html',
        form=form,
        magazines=magazines,
        success_msg=request.args.get('success_msg')
    )

@crud_magazines.route('/editar_periodicos/', methods=['GET', 'POST'])
@login_required
def edit_magazine():

    allowed_extensions = ['jpg', 'png']

    form = EditMagazinesForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.publications_dao()
    magazines = pfactory.publications_dao().find_one()
    magazines = dict(magazines)['magazines']
    magazines = dumps(magazines)

    if form.validate_on_submit() and form.create.data:
        index = str(form.index.data)
        if form.cover.data is not None:
            cover = form.cover.data
            path = os.path.normpath("static/assets/magazines")
            filename = secure_filename(cover.filename)
            if filename.count('.') > 1:
                return redirect(
                    url_for(
                        'crud_magazines.edit_magazine',
                        success_msg='Nome do arquivo da capa contem mais de um . por favor corrija isso'
                    )
                )
            name, extension = filename.split('.')
            uploadFiles(cover, path, filename)
            new_magazine = {
                'name': form.name.data,
                'coverFile': filename,
                'description': form.description.data,
                'issn' : form.issn.data
            }
            dao.find_one_and_update(None, {
                '$set': {'magazines.' + index : new_magazine}
            })
        else:
            dao.find_one_and_update(None, {
                '$set' : {'magazines.' + index + '.issn' : form.issn.data}
            })
            dao.find_one_and_update(None, {
                '$set' : {'magazines.' + index + '.description' : form.description.data}
            })
            dao.find_one_and_update(None, {
                '$set' : {'magazines.' + index + '.name' : form.name.data}
            })

        return redirect(
            url_for(
                'crud_magazines.edit_magazine',
                magazines=magazines,
                success_msg='Periódico editado com sucesso.'
            )
        )


    return render_template(
        'admin/edit_magazine.html',
        form=form,
        magazines=magazines,
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

