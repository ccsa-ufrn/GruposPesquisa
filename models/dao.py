"""
All data **MUST** be only manipulated through this middleware,
and not directly using Pymongo nor other API wrapper. And also,
all DAOs **SHOULD** be created using factory methods.
"""
from threading import Thread
import sys

from models.clients.mongo import DB
from models.clients import api_sistemas

class AbstractDAO(object):

    def __init__(self, collection: str):
        raise NotImplementedError("Tried to create instance from abstract class.")

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def count(self, conditions: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")


    def insert_one(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def insert_many(self, document: list):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def update(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def delete(self, document: dict):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")



class GenericMongoDAO(AbstractDAO):
    """
    Implements a generic middleware for accessing MongoDB.

    Note that this instance itself don't represent anything at domain,
    it's just useful for accessing dictionaries that stands for documents
    from a certain database collection.
    """

    def __init__(self, collection: str, owner_post_graduation_id: str = None):
        """
        Don't use this constructor directly as you're probably doing now.
        Use its factory instead!

        Create an instance for starting using data access methods.

        All data access will assume as context the given collection.
        Also, will add a 'ownerProgram' search parameter as
        owner_post_graduation_id to all data filterings. Collection
        name must never be None.
        """
        self.collection = collection
        self.owner_post_graduation_id = owner_post_graduation_id

    def find_all(self):
        """
        Gets a list of all the documents from the collection.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        return DB[self.collection].find_all()

    def find_one(self, conditions: dict = None):
        """
        Gets a single found document with the given conditions, returns it as dict.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find_one(conditions)

    def find(self, conditions: dict = None):
        """
        Filters documents from database collection. The given dictionary param
        represents the filter json. Returns a list of dicts, where each of them
        is a found document.
        TODO: retrieve only logical alive documents (maybe a 'alive_only=True' param?)
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
	#Ex: return DB['gradesOfSubjects'].find(5a15ca97d818ecf5068593c9) <- Sendo esse número o id do programa de pós-graduação
        return DB[self.collection].find(conditions)

    def count(self, conditions: dict = None):
        """
        Find the number of documents inside collection
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].count(conditions)


    def insert_one(self, conditions: dict, document: dict):
        """
        Insert a document as dict into the collection and returns its new id if it worked.
        TODO: insert an alive document
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].insert(document)

    def insert_many(self, document: list):
        """
        TODO: Insert a list of documents into the collection and returns a list of their
        new ids if it worked.
        """
        raise NotImplementedError("Tried to call an update function without implementing it.")

    def find_one_and_update(self, conditions: dict, update: dict):
        """
        Finds a single document and updates it, returning the original.
        """
        if conditions is None:
            conditions = {}
        if self.owner_post_graduation_id is not None:
            conditions['ownerProgram'] = self.owner_post_graduation_id
        return DB[self.collection].find_one_and_update(conditions, update)

    def delete(self, document: dict):
        """
        TODO: Logical delete. So the document still recorded at persistence,
        but can no longer be retrieved using regular CRUD methods.
        """
        raise NotImplementedError("Need to implement update function for logical deleting it.")

class ProfessorsSigaaDAO(AbstractDAO):

    def __init__(self):
        self.ENDPOINT = api_sistemas.API_URL_ROOT
        self._professors = []
        self._bearer_token = None

    def find_all(self):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find_one(self, conditions):
        raise NotImplementedError("Not implemented method inherited from an abstract class.")

    def find(self, conditions: dict = {}):
        bearer_token = api_sistemas.retrieve_token()
        units = ['63','11612', '161', '163', '79', '84', '160', '162', '5393', '9750']
        list_of_professors = []
        for unit in units:
            list_of_professors.extend(self.get_professor(unit, bearer_token))
        return list_of_professors

    def get_professor(self, id_unit: str, bearer_token: str):
        url = api_sistemas.API_URL_ROOT
        url += '/docente/v1/docentes?id-unidade={id_unit}&limit=100&id-ativo=1'
        url = url.format(id_unit=id_unit)
        results = api_sistemas.get_public_data(url, bearer_token)
        print(len(results), file=sys.stderr)
        list_without_duplicates = []
        for result in results:
            if not any(professor.get('cpf', None) == result['cpf'] for professor in list_without_duplicates):
                list_without_duplicates.append(result)
        print(len(list_without_duplicates), file=sys.stderr)
        return list_without_duplicates

    def insert_one(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def insert_many(self, document: list):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def update(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")

    def delete(self, document: dict):
        raise NotImplementedError("Data from SIGAA are read-only.")
