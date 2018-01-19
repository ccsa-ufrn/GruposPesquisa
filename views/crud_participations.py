"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import ResearchGroupFactory

from settings.extensions import ExtensionsManager

from views.forms.content import ParticipationsInEventsForm

from bson.json_util import dumps
import json
import datetime

crud_participations = Blueprint('crud_participations', __name__, url_prefix='/admin')

###############################################################################
#Adicionar deletar e editar intercâmbios
###############################################################################

@crud_participations.route('/intercambios/', methods=['GET', 'POST'])
@login_required
def participations():
    """Render a view for integrations lists."""

    form = ParticipationsInEventsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()

    if form.validate_on_submit() and form.create.data:
        new_participation = {
            'title': form.title.data,
            'description': form.description.data,
            'year': form.year.data,
            'international': form.location.data
        }

        dao.find_one_and_update(None, {
            '$push': {'participationsInEvents': new_participation}
        })

        return redirect(
            url_for(
                'crud_participations.participations',
                success_msg='Intercâmbio adicionado adicionado com sucesso.'
            )
        )

    return render_template(
        'admin/participations.html',
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_participations.route('/deletar_intercâmbio/', methods=['GET', 'POST'])
@login_required
def delete_participations():
    """
    Render a delete participation form.
    """

    form = ParticipationsInEventsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)


    if form.validate_on_submit():
        dao.find_one_and_update(None , {
            '$set': {'participationsInEvents.' + index + '.deleted' : ""}
        })

        return redirect(
            url_for(
                'crud_participations.delete_participations',
                participations=json,
                success_msg='Participação deletada com sucesso'
            )
        )
    return render_template(
        'admin/delete_participations.html',
        form=form,
        participations=json,
        success_msg=request.args.get('success_msg')
    )

@crud_participations.route('/editar_intercâmbio/', methods=['GET', 'POST'])
@login_required
def edit_participations():
    """
    Render a edit participation form.
    """

    form = ParticipationsInEventsForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.integrations_infos_dao()
    json = pfactory.integrations_infos_dao().find_one()
    json = dict(json)
    json = dumps(json)
    index = str(form.index.data)

    if form.validate_on_submit() and form.create.data:
        year = int(form.year.data)
        new_participation = {
            'title': form.title.data,
            'description': form.description.data,
            'year': year,
            'international': form.location.data
        }

        dao.find_one_and_update(None, {
            '$set': {'participationsInEvents.' + index : new_participation}
        })

        return redirect(
            url_for(
                'crud_participations.edit_participations',
                participations=json,
                success_msg='Participação editada com sucesso'
            )
        )
    return render_template(
        'admin/edit_participations.html',
        form=form,
        participations=json,
        success_msg=request.args.get('success_msg')
    )
