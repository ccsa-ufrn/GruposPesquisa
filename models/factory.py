"""
All DAOs should be called using this module, instead
of directly call their own constructor.

A factory of Data Access Objects.
"""

from models.dao import GenericMongoDAO
import sys

# constants for collection names in mongodb

_COLLECTION_OF_RESEARCH_GROUPS = 'researchGroups'
_COLLECTION_OF_FINAL_REPORTS = 'finalReports'
_COLLECTION_OF_INTEGRATIONS_INFOS = 'integrationsInfos'
_COLLECTION_OF_BOARDS_OF_STAFFS = 'boardsOfStaffs'
_COLLECTION_OF_OFFICIAL_DOCUMENTS = 'officialDocuments'
_COLLECTION_OF_ATTENDANCES = 'attendances'
_COLLECTION_OF_CALENDAR = 'calendar'
_COLLECTION_OF_PUBLICATIONS = 'publications'
_COLLECTION_OF_PROJECTS = 'projects'

# factory methods

class ResearchGroupFactory(object):
    """
    Provide factory methods for data access objects to research groups.
    """

    def __init__(self, name='noNameProvided'):
        """
        If a parameter is given (program's initials), all data access objects
        created will be implictly searching for the found program.
        """
        self.research_group = self.research_groups_dao().find_one({
            'name': name
        })

        if self.research_group is not None:
            self.mongo_id = self.research_group['_id']
        else:
            self.mongo_id = None


    def research_groups_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_RESEARCH_GROUPS)

    def final_reports_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_FINAL_REPORTS, self.mongo_id)

    def publications_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_PUBLICATIONS, self.mongo_id)

    def integrations_infos_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_INTEGRATIONS_INFOS, self.mongo_id)

    def calendar_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_CALENDAR, self.mongo_id)

    def boards_of_staffs_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_BOARDS_OF_STAFFS, self.mongo_id)

    def official_documents_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_OFFICIAL_DOCUMENTS, self.mongo_id)

    def attendances_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_ATTENDANCES, self.mongo_id)

    def projects_database_dao(self):
        """ Gets an instance of a data access object for a certain collection """
        return GenericMongoDAO(_COLLECTION_OF_PROJECTS, self.mongo_id)
