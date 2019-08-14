"""
config.py
-----------
*Flask Configuration file*
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

POSTGRES = {
    'host': 'localhost',
    'port': '5432',
    'user': 'user',
    'pw': '***',
    'db': 'authorizer'
}
from db import *


class Conf():
    """
    *Conf Class for import*
    """
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DEBUG = True
    SECRET_KEY = os.urandom(12)
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
