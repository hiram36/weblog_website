#!flask/bin/python3

from migrate.versioning import api
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO

from config import Config

from app import pgdb
import os.path

def db_create():
    pgdb.create_all()

    if not os.path.exists(Config.SQLALCHEMY_MIGRATE_REPO):
        api.create(Config.SQLALCHEMY_MIGRATE_REPO, 'database repository')
        api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    else:
        api.version_control(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, api.version(Config.SQLALCHEMY_MIGRATE_REPO))

def main():
    db_create()

if __name__ == '__main__':
    main()
