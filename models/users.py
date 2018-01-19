"""
Has some functionalities about user authentication and
session management.
"""

from models.factory import ResearchGroupFactory
from bcrypt import checkpw, hashpw, gensalt
import sys
import requests
import json


class User(object):
    """
    Implements some properties and methods (a few of them according
    to Flask-Login extension).
    """

    def __init__(self):
        self._id = None
        self._group_name = None
        self._nick = None
        self._full_name = None
        self._role = None
        self._email = None
        self._password = None
        self.__is_authenticated = None
        self.__is_active = None
        self.__is_anonymous = None

    def authenticate(self, raw_password_try):
        """Try to log in using an raw password (not hashed yet), and return True"""
        if User._check_password(self._password, raw_password_try):
            self.__is_authenticated = True
        else:
            self.__is_authenticated = False

        return self.__is_authenticated

    @staticmethod
    def _check_password(real_hashed_password, raw_password_try):
        """Hash the raw_try_pass and check if they match. Return a boolean result."""
        return checkpw(raw_password_try.encode('utf-8'), real_hashed_password)

    @staticmethod
    def __hash_password(raw_password):
        """Encode and convert a raw password into a hash. Return a string result."""
        return hashpw(raw_password.encode('utf-8'), gensalt(14))

    @property
    def id(self):
        """An unique representation of a certain user."""
        return '{}@{}'.format(self._nick, self._group_name)

    @property
    def nick(self):
        """An user nickname."""
        return self._nick

    @property
    def full_name(self):
        """User's full real name."""
        return self._full_name

    @property
    def password(self):
        """An user password, already hashed."""
        return self._password

    @property
    def role(self):
        """Its employement position."""
        return self._role

    @property
    def email(self):
        """Valid contact e-mail."""
        return self._email

    @property
    def group_name(self):
        """Research group that the user manages"""
        return self._group_name.upper()

    @property
    def is_authenticated(self):
        """
        This property should return True if the user is authenticated,
        i.e. they have provided valid credentials.
        (Only authenticated users will fulfill the criteria of
        login_required.)
        """
        return self.__is_authenticated

    @property
    def is_active(self):
        """
        This property should return True if this is an active
        user - in addition to being authenticated, they also have
        activated their account, not been suspended, or any condition
        your application has for rejecting an account. Inactive
        accounts may not log in (without being forced of course).
        """
        return self.__is_active

    @property
    def is_anonymous(self):
        """
        This property should return True if this is an anonymous user.
        (Actual users should return False instead.)
        """
        return self.__is_anonymous

    def get_id(self):
        """
        This method must return a unicode that uniquely identifies
        this user, and can be used to load the user from the
        user_loader callback. Note that this must be a
        unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode.
        """
        return self.id

    @staticmethod
    def get(nick, authenticated=False):
        """Return an User from database. If failed, None."""
        try:
            condition = {'users.nick': nick}
            pfactory = ResearchGroupFactory()
            dao = pfactory.research_groups_dao()
            research_group = list(dao.find(condition))
            if research_group:
                group_name = research_group[0]['name']
            else:
                return None
            for user in research_group[0]['users']:
                if nick.lower() == user['nick'].lower():
                    found_user = User()
                    found_user._nick = user['nick']
                    found_user._group_name = group_name
                    found_user._password = user['password'].encode('utf-8')
                    found_user._full_name = user['fullName']
                    found_user._role = user['role']
                    found_user._email = user['email']
                    found_user.__is_authenticated = authenticated
                    found_user.__is_active = True
                    found_user.__is_anonymous = False
                    return found_user
            return None
        except (TypeError, AttributeError):
            return None
