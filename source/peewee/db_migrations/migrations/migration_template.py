# MIGRATION_NAME = "example_migration"

# def run_migration(database, logger):
#     try:
#         logger.info(f"Running migration: {MIGRATION_NAME}")
#         with database.atomic():
#             # Add your migration code here
#             pass
#         logger.info("Migration completed successfully")
#         return True
#     except Exception as exc:
#         logger.error(f"Migration failed: {exc}")
#         return False