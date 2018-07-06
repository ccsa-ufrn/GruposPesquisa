"""
Routes and views for articles CRUD.
"""

import json
import sys

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request, session, jsonify
from flask_cors import cross_origin

from models.factory import ResearchGroupFactory 

from settings.extensions import ExtensionsManager


from bson.json_util import dumps
from bson.objectid import ObjectId

avaliation_form = Blueprint('avaliation_form', __name__, url_prefix='/admin')

@avaliation_form.route('/formulario_avaliacao/', methods=['GET'])
@ExtensionsManager.csrf.exempt
@login_required
def submit_avaliation_form():
    return render_template(
    'admin/avaliation_form.html',
    )

@avaliation_form.route('/formulario_avaliacao_final/', methods=['POST'])
@ExtensionsManager.csrf.exempt
@cross_origin()
def submit_avaliation_form_final():
    formResult = request.get_json()
    formResult['success'] = 'true' 
    pfactory = ResearchGroupFactory(formResult['groupAccount'])
    if '_id' not in formResult:
        formResult['_id'] = ObjectId()
        dao = pfactory.avaliation_form_dao()
        dao.find_one_and_update(None, {
            '$push': {'formYear': formResult}
        })

    formResult = dict(formResult)
    formResult = dumps(formResult)
    return jsonify(formResult)