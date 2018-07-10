"""
Routes and views for articles CRUD.
"""

import json
import sys
import random
import string

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_cors import cross_origin

from models.factory import ResearchGroupFactory 

from settings.extensions import ExtensionsManager


from bson.json_util import dumps, loads
from bson.objectid import ObjectId

avaliation_form = Blueprint('avaliation_form', __name__, url_prefix='/admin')

@avaliation_form.route('/formulario_avaliacao/', methods=['GET'])
@ExtensionsManager.csrf.exempt
@login_required
def submit_avaliation_form():
    form_type = request.args.get('form_type')
    if form_type == 'formYear':
        return render_template(
        'admin/avaliation_form.html',
        new=request.args.get('new'),
        )
    else:
        return render_template(
        'admin/avaliation_form_four_years.html',
        new=request.args.get('new'),
        )

@avaliation_form.route('/formulario_avaliacao_final/', methods=['POST'])
@ExtensionsManager.csrf.exempt
@cross_origin()
def submit_avaliation_form_final():
    formResult = request.get_json()
    formResult['success'] = 'true' 
    pfactory = ResearchGroupFactory(formResult['groupAccount'])
    if '_id' not in formResult:
        formResult['_id'] = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
        formResult.pop('index', None)
        form_type = formResult['form_type']
        formResult.pop('form_type', None)
        dao = pfactory.avaliation_form_dao()
        dao.find_one_and_update(None, {
            '$push': {form_type: formResult}
        })
        return jsonify(dumps({"success":"true"}))
    else:
        dao = pfactory.avaliation_form_dao()
        index = int(formResult['index']) - 1
        formResult.pop('index', None)
        form_type = formResult['form_type']
        formResult.pop('form_type', None)
        dao.find_one_and_update(None, {
            '$set' : { form_type + '.' + str(index) : formResult }
        })
        return jsonify(dumps({"success":"true"}))


@avaliation_form.route('/informacoes_formulario/', methods=['POST'])
@ExtensionsManager.csrf.exempt
@cross_origin()
def get_information():
    formResult = request.get_json()
    pfactory = ResearchGroupFactory(formResult['groupAccount'])
    forms = pfactory.avaliation_form_dao().find_one()
    forms = dict(forms)
    index = int(formResult['index']) - 1
    forms = forms[(formResult['form_type'])][index]
    if forms['_id'] == formResult['id']:
        forms = dumps(forms)
        return jsonify(forms)
    else:
        return jsonify({'not_found': 'not_found'})

@avaliation_form.route('/listar_formularios/', methods=['GET', 'POST'])
@ExtensionsManager.csrf.exempt
@cross_origin()
def list_forms():
    form_type = request.args.get('form_type') 
    form_result = request.get_json()
    pfactory = ResearchGroupFactory(current_user.group_name)
    forms = pfactory.avaliation_form_dao().find_one()[form_type]

    return render_template(
        'admin/list_forms.html',
        forms = forms,
        form_type=request.args.get('form_type')
    )
