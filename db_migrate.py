#!flask/bin/python3
import imp
from migrate.versioning import api
from app import pgdb
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
from config import Config

def db_migrate():
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    migration = Config.SQLALCHEMY_MIGRATE_REPO + ('/versions/%03d_migration.py' % (v+1))

    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO, tmp_module.meta, pgdb.metadata)
    open(migration, "wt").write(script)

    api.upgrade(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)
    v = api.db_version(Config.SQLALCHEMY_DATABASE_URI, Config.SQLALCHEMY_MIGRATE_REPO)

    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))

def main():
    db_migrate()

if __name__ == '__main__':
    main()
