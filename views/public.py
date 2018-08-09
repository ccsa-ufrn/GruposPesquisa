"""
Routes and views for public pages about Post Graduation Programs.
"""
import sys

from flask import Blueprint, render_template, redirect, \
current_app, request, jsonify, url_for
from pymongo.errors import ServerSelectionTimeoutError

from scraping.institutional_repository import RIScraper
from models.clients.util import keyring

from models.factory import ResearchGroupFactory

from bson.json_util import dumps


app = Blueprint('public', __name__, static_folder='static', url_prefix='')

@app.route('/')
def root():
    """
    Render a root page for public access.
    """
    return render_template(
        'public/index.html',
        std=get_std_for_template(None),
    )




@app.route('/<string:name>/')
def home(name):
    """
    Render a research group page.

    Try to find which group has been requested.

    If it's here: signed in Juno, show its main page,

    If couldn't find which program has been requested, show a 404 page error.
    """

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    # renders an own page or redirect to another (external/404)?
    if research_group is None:
        return page_not_found()

    # query google maps api
    google_maps_api_dict = keyring.get(keyring.GOOGLE_MAPS)

    google_maps_api_key = 'none'
    if google_maps_api_dict is not None:
        google_maps_api_key = google_maps_api_dict['key']

    # search for home data
    final_reports = pfactory.final_reports_dao().find_one()
    calendar = pfactory.calendar_dao().find_one()['events']
    selections = []
    events = []
    for event in range(len(calendar)):
        if "deleted" not in calendar[event]:
            if "Seleção" in calendar[event]['title']:
                selections.append(calendar[event])
            else:
                events.append(calendar[event])
    news = pfactory.news_dao().find_one()
    news = news['news']
    final_reports = final_reports['scheduledReports']
    integrations_infos = pfactory.integrations_infos_dao().find_one()
    if integrations_infos is None:
        integrations_infos = {
            'name': "",
            'name': "",
            'logoFile': "",
        }
        institutions_with_covenant = integrations_infos
    else:
        institutions_with_covenant = integrations_infos['institutionsWithCovenant']
    attendance = pfactory.attendances_dao().find_one()
    if attendance is None:
        attendance = {
            'location' : {
                'building' : '',
                'floor' : '',
                'room' : '',
                'opening' : ''
                },
            'email' : '',
            'phones' : {
                'type' : '',
                'number' : ''
                }
        }

    # ready... fire!
    return render_template(
        'public/home.html',
        std=get_std_for_template(research_group),
        google_maps_api_key=google_maps_api_key,
        final_reports=final_reports,
        events=events,
        news=news,
        institutions_with_covenant=institutions_with_covenant,
        attendance=attendance,
        selections=selections,
    )

@app.route('/<string:name>/documents/<string:filename>/')
def download_documents(name, filename):
    """
    Open a file from static folder.
    """
    return current_app.send_static_file('upload_files/' + name.lower() + '/' + filename)

@app.route('/<string:name>/intercambios/')
def view_participations(name):
    """Render a view for integrations lists."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    integrations_infos = pfactory.integrations_infos_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/participations.html',
        std=get_std_for_template(research_group),
        integrations_infos=integrations_infos
    )

@app.route('/<string:name>/convenios/')
def view_covenants(name):
    """Render a view for integrations lists."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    integrations_infos = pfactory.integrations_infos_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/covenants.html',
        std=get_std_for_template(research_group),
        integrations_infos=integrations_infos
    )

@app.route('/<string:name>/fomentos/')
def view_fomentation(name):
    """Render a view for fomentation."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    integrations_infos = pfactory.integrations_infos_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/fomentation.html',
        std=get_std_for_template(research_group),
        integrations_infos=integrations_infos
    )

@app.route('/<string:name>/calendario/')
def view_calendar(name):
    """Render a view for calendar."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    calendar_info = pfactory.calendar_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/calendar.html',
        std=get_std_for_template(research_group),
        calendar_info=calendar_info
    )

@app.route('/<string:name>/equipe/')
def view_staffs(name):
    """Render a view for staff list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    board_of_staffs = pfactory.boards_of_staffs_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/staffs.html',
        std=get_std_for_template(research_group),
        board_of_staffs=board_of_staffs
    )

@app.route('/<string:name>/projetos/')
def view_projects(name):
    """Render a view for projects list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group
    projects = pfactory.projects_database_dao().find()
    projects = list(projects)
    for project in projects:
        coordinators_names = []
        for member in project['members']:
            if 'Coordenador(a)' in member['project_role']:
                coordinators_names.append(member)
                project['members'].remove(member)
        project['coordinators_names'] = coordinators_names

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/projects.html',
        std=get_std_for_template(research_group),
        projects=projects
    )


@app.route('/<string:name>/livros/')
def view_books(name):
    """Render a view for books list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/books.html',
        std=get_std_for_template(research_group),
        publications=publications
    )


@app.route('/<string:name>/capitulos/')
def view_chapters(name):
    """Render a view for chapters list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/chapters.html',
        std=get_std_for_template(research_group),
        publications=publications
    )

@app.route('/<string:name>/artigos/')
def view_articles(name):
    """Render a view for articles list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/articles.html',
        std=get_std_for_template(research_group),
        publications=publications
    )

@app.route('/<string:name>/periodicos/')
def view_magazines(name):
    """Render a view for magazines list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    publications = pfactory.publications_dao().find_one()

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/magazines.html',
        std=get_std_for_template(research_group),
        publications=publications
    )


@app.route('/<string:name>/documentos/regimentos')
def view_documents_regiments(name):
    """Render a view for documents list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    documents = pfactory.official_documents_dao().find({'category':'regimento'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_regiments.html',
        std=get_std_for_template(research_group),
        documents=documents
    )

@app.route('/<string:name>/documentos/atas')
def view_documents_atas(name):
    """Render a view for documents list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    documents = pfactory.official_documents_dao().find({'category':'ata'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_atas.html',
        std=get_std_for_template(research_group),
        documents=documents
    )

@app.route('/<string:name>/documentos/outros')
def view_documents_others(name):
    """Render a view for documents list."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    documents = pfactory.official_documents_dao().find({'category':'outros'})

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/documents_others.html',
        std=get_std_for_template(research_group),
        documents=documents
    )

@app.route('/<string:name>/noticias/')
def view_news(name):
    """Render a view for news viewing."""

    pfactory = ResearchGroupFactory(name)
    research_group = pfactory.research_group

    id = request.args.get('id')
    news = pfactory.news_dao().find_one()['news']
    fullNews = next(piece for piece in news if piece['id'] == id)

    # renders an own page or redirect to another (external/404)?
    return render_template(
        'public/news.html',
        std=get_std_for_template(research_group),
        fullNews=fullNews 
    )

# AUX
def get_std_for_template(research_group, give_me_empty=False):
    """
    Return default template stuff for jinja to render.

    Freely put None if theres no research_group dict.
    But if there's one, must be the found by DAOs
    and requested by user.

    Must be called like this in every template:
        return render_template('MYTEMPLATE.html', std=get_std_for_template(None), ...)
    That said, there will always be a std dict in jinja environments.

    Jinja will have following template vars, if you called it right:
        std.research_group (dict for current given post graduation)
        std.research_groups_registered (dict for the post graduations available at minerva)
        std.research_groups_unregistered (dict for post graduations unavailable at minerva)
    They can be None if nothing has found from database or provided by function args.

    Jinja will have the following template vars, if you called it with give_me_empty=True:
        std.research_group == None
        std.research_groups_registered == []
        std.research_groups_unregistered == []
    """
    if give_me_empty:
        return {
            'research_group': None,
            'research_groups_registered': [],
            'research_groups_unregistered': [],
        }
    else:
        pfactory = ResearchGroupFactory()
        research_groups_registered = pfactory.research_groups_dao().find({'isSignedIn': True})
        return {
            'research_group': research_group,
            'research_group_registered' : research_groups_registered
        }



@app.route('/404')
@app.errorhandler(404)
def page_not_found(error=None):
    """Render page not found error."""

    print(str(error))
    return render_template('404.html', std=get_std_for_template(None)), 404

@app.errorhandler(ServerSelectionTimeoutError)
def pymongo_exception_handler(error):
    """Render page for PyMongo errors."""
    print("ERROR for PyMongo: MongoDB took too long to answer, is its service available, running and can be reached?")
    # never renders it... =[ why?
    return render_template('public/500.html', std=get_std_for_template(None), give_me_empty=True), 500
