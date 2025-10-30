# MIGRATION_NAME = "001_initial"

from librepy.pybrex.values import APP_NAME

MIGRATION_NAME = "001_initial"
APPLICATION_SCHEMA = APP_NAME

def run_migration(database, logger):
    try:
        logger.info(f"Running migration: {MIGRATION_NAME}")

        # Ensure application schema exists and set search_path for this session/transaction
        database.execute_sql(f'CREATE SCHEMA IF NOT EXISTS "{APPLICATION_SCHEMA}";')
        database.execute_sql(f'SET search_path TO "{APPLICATION_SCHEMA}", public;')

        # Dynamically discover all app models (subclasses of BaseModel) in app/data/model.py
        import inspect
        from librepy.app.data import model as app_models
        from librepy.peewee.db_model.base_model import BaseModel

        models = [
            cls for _, cls in inspect.getmembers(app_models, inspect.isclass)
            if cls is not BaseModel and issubclass(cls, BaseModel)
        ]
        logger.info(f"Discovered {len(models)} models for migration: {[m.__name__ for m in models]}")

        # Temporarily bind the discovered models to the provided database
        original_dbs = {m: m._meta.database for m in models}
        for m in models:
            m._meta.database = database

        try:
            with database.atomic():
                database.create_tables(models)
        finally:
            # Restore original database bindings
            for m, orig_db in original_dbs.items():
                m._meta.database = orig_db

        logger.info("Migration completed successfully")
        return True
    except Exception as exc:
        logger.error(f"Migration failed: {exc}")
        return False
