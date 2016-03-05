#!flask/bin/python3
from migrate.versioning import api
from config import Config

def db_upgrade():
    api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    print ('Current database version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)))

def main():
    db_upgrade()


if __name__ == '__main__':
    main()
