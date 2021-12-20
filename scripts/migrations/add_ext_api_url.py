from playhouse.migrate import PostgresqlMigrator, migrate
from src.database import database, Company, Trips
migrator = PostgresqlMigrator(database)


def run_migration():
    migrate(
        migrator.add_column('company', 'ext_api_key', Company.ext_api_key),
    )


if __name__ == '__main__':
    run_migration()
