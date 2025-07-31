# Vendored Peewee ORM (subset)

This directory contains a **small, self-contained copy of selected modules from the
[Peewee ORM](https://github.com/coleifer/peewee)**.  We vendor only the pieces
we actively use so that our application can run inside LibreOffice’s Python
runtime without requiring external packages.

Included components
-------------------
1. `peewee.py` – core ORM implementation.
2. `playhouse/migrate.py` – schema-migration helpers (DDL generator).
3. `playhouse/reflection.py` – database introspection utilities used by `pwiz`.
4. `pwiz.py` & `run_pwiz.py` – code-generator that builds model classes from an
   existing database.
5. `sdbc_dbapi.py` – **DB-API 2.0 bridge** that wraps LibreOffice UNO SDBC
   connections so they look like a standard Python database driver.
6. `sdbc_peewee.py` – adapter that lets Peewee talk to `sdbc_dbapi` by
   implementing a minimal `Database` subclass.

Note:
-------------------
1. Only use migrate for instances when the PostgreSQL database installation is > version 15.
