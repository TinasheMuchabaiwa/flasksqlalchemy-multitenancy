import os
from app import db
from flask import jsonify
from sqlalchemy import text, MetaData, Table, Column, inspect
from sqlalchemy.exc import IntegrityError


def create_organization_schema(name: str):
    statement = text(f"CREATE SCHEMA IF NOT EXISTS {name}")
    connection = db.engine.connect()
    transaction = connection.begin()
    try:
        connection.execute(statement)
        transaction.commit()
    except IntegrityError:
        transaction.rollback()
    finally:
        connection.close()


# def create_organization_tables(name, organization_id):
#     connection = db.engine.connect()
#     transaction = connection.begin()
#     try:
#         metadata = MetaData(schema='public')
#         metadata.reflect(bind=db.engine)

#         for table_name, table in metadata.tables.items():
#             if table_name != 'organization' and table_name != 'alembic_version':
#                 new_table_name = f"{name}.{table_name}"
#                 new_columns = [Column(column.name, column.type, nullable=column.nullable) for column in table.columns]
#                 new_table = Table(new_table_name, metadata, *new_columns, schema=name)
#                 new_table.create(db.engine)
#                 connection.execute(new_table.insert().from_select(new_table.columns.keys(), table.select()))
#                 connection.execute(text(f"ALTER TABLE {table_name} OWNER TO {os.getenv('DB_USER')};"))
#                 connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS organization_id integer;"))
#                 connection.execute(text(f"UPDATE {table_name} SET organization_id = {organization_id};"))
#                 connection.execute(text(f"ALTER TABLE {new_table_name} ADD CONSTRAINT {new_table_name}_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization (id);"))

#     except IntegrityError:
#         transaction.rollback()
#     finally:
#         connection.close()


def create_organization_tables(name, organization_id):
    connection = db.engine.connect()
    transaction = connection.begin()
    try:
        # Retrieve the list of table names from the 'public' schema
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names(schema='public')

        for table_name in table_names:
            if table_name != 'organization':
                if table_name != 'alembic_version':
                    new_table_name = f"{name}.{table_name}"

                    # Generate the CREATE TABLE statement with the new table name and organization_id column
                    create_table_sql = text(f"CREATE TABLE {new_table_name} (LIKE public.{table_name} INCLUDING CONSTRAINTS);")
                    connection.execute(create_table_sql)

                    # Add foreign key constraint to the new table
                    add_fk_constraint_sql = text(f"ALTER TABLE {new_table_name} ADD CONSTRAINT {table_name}_organization_id_fkey FOREIGN KEY (organization_id) REFERENCES public.organization (id);")
                    connection.execute(add_fk_constraint_sql)
        transaction.commit()

    except IntegrityError:
        transaction.rollback()
    finally:
        connection.close()
