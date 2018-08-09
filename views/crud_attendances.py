"""
Routes and views for articles CRUD.
"""

from flask_login import login_required, current_user
from flask import Blueprint, render_template, redirect, url_for, request

from models.factory import ResearchGroupFactory

from settings.extensions import ExtensionsManager

from views.forms.content import AttendanceForm, DescriptionForm

from bson.json_util import dumps
from bson.objectid import ObjectId
import json
import sys

crud_attendances = Blueprint('crud_attendances', __name__, url_prefix='/admin')

@crud_attendances.route('/editar_contato/', methods=['GET', 'POST'])
@login_required
def edit_attendance():

    form = AttendanceForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.attendances_dao()
    json = pfactory.attendances_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        new_attendance = {
            'location' : {
                'building' : form.building.data,
                'floor' : form.floor.data,
                'room' : form.room.data,
                'opening' : form.opening.data
            },
            'email': form.email.data,
            'phones' : {
                '0' : {
                    'type' : form.type1.data,
                    'number': form.phone1.data
                },
                '1' : {
                    'type': form.type2.data,
                    'number': form.phone2.data
                },
                '2' : {
                    'type': form.type3.data,
                    'number': form.phone3.data
                }
            }
        }

        dao.find_one_and_update({'_id' : ObjectId(form.attendance_id.data)}, {
            '$set': new_attendance
        })

        return redirect(
            url_for(
                'crud_attendances.edit_attendance',
                success_msg='Contato editado com sucesso.'))

    return render_template(
        'admin/edit_attendance.html',
        attendance=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )

@crud_attendances.route('/editar_descrições/', methods=['GET', 'POST'])
@login_required
def edit_description():

    form = DescriptionForm()

    pfactory = ResearchGroupFactory(current_user.group_name)
    dao = pfactory.research_groups_dao()
    json = pfactory.research_groups_dao().find_one()
    json = dict(json)
    json = dumps(json)

    if form.validate_on_submit() and form.create.data:
        new_information = {
            'descriptionSmall' : form.description_small.data,
            'descriptionBig' : form.description_big.data,
            'anyText' : form.any_text.data,
            'firstImage' : form.first_image.data,
            'secondImage': form.second_image.data,
        }

        dao.find_one_and_update({'_id' : ObjectId(current_user.group_id)}, {
            '$set': new_information
        })

        return redirect(
            url_for(
                'crud_attendances.edit_description',
                success_msg='Descrições editadas com sucesso.'))

    return render_template(
        'admin/edit_description.html',
        description=json,
        form=form,
        success_msg=request.args.get('success_msg')
    )
