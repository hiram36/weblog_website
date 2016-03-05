#!flask/bin/python3
from migrate.versioning import api
from config import Config

def db_downgrade():
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    api.downgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, v - 1)
    print ('Current database version: ' + str(api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)))


def main():
    db_downgrade()


if __name__ == '__main__':
    main()
