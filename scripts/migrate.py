from peewee import FloatField
from playhouse.migrate import PostgresqlMigrator, migrate
from src.database import database, Company, Trips, Locations
migrator = PostgresqlMigrator(database)


def run_migration():
    migrate(
        # migrator.add_column('company', 'ext_api_key', Company.ext_api_key),
        # migrator.add_column('trips', 'total_meters', Trips.total_meters),
        # migrator.rename_column('trips', 'total_kms', 'total_meters'),
        # migrator.rename_column('trips', 'kms_travelled', 'meters_traveled'),
        # migrator.alter_column_type('trips', 'total_meters', FloatField()),
        # migrator.alter_column_type('trips', 'meters_traveled', FloatField()),
        migrator.rename_column(
            'locations', 'gps_location', 'location_data'),
    )


if __name__ == '__main__':
    run_migration()
