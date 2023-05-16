from flask import jsonify, url_for, abort
from http import HTTPStatus
from .models import User, Organization
from app import db
from app.database import create_organization_schema, create_organization_tables
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker


def create_organization(organization_data: dict):
    name = organization_data.get("name")
    if Organization.find_by_name(name):
        response = jsonify(
            status="fail",
            message="Organization already exists."
        )
        response.status_code = HTTPStatus.CONFLICT
        return response

    new_organization = Organization(**organization_data)
    db.session.add(new_organization)
    db.session.commit()

    create_organization_schema(name)
    create_organization_tables(name, new_organization.id)

    response = jsonify(
        status="success",
        message="successfully registered",
    )
    response.status_code = HTTPStatus.CREATED
    response.headers["Location"] = url_for(
        "api.organization", id=new_organization.id, _external=True
    )
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"
    return response


# def create_user(user_data: dict):
#     name = user_data.get("name")
#     if User.find_by_name(name):
#         response = jsonify(
#             status="fail",
#             message="User already exists."
#         )
#         response.status_code = HTTPStatus.CONFLICT
#         return response

#     organization_id = user_data.get("organization_id")
#     if not Organization.query.get(organization_id):
#         response = jsonify(
#             status="fail",
#             message="Organization does not exist."
#         )
#         response.status_code = HTTPStatus.NOT_FOUND
#         return response

#     # set the organization schema as the current schema
#     statement = text(f"SET search_path TO {Organization.query.get(organization_id).name}")
#     connection = db.engine.connect()
#     transaction = connection.begin()
#     try:
#         connection.execute(statement)
#         new_user = User(**user_data)
#         db.session.add(new_user)
#         db.session.commit()
#         transaction.commit()
#     except IntegrityError:
#         transaction.rollback()
#         response = jsonify(
#             status="fail",
#             error="IntegrityError",
#         )
#         response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
#         return response
#     except Exception as e:
#         transaction.rollback()
#         response = jsonify(
#             status="fail",
#             error=str(e),
#         )
#         response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
#         return response
#     finally:
#         connection.close()


from sqlalchemy import text

def create_user(user_data: dict):
    organization_id = user_data.get("organization_id")
    organization = Organization.find_by_id(organization_id)
    if not organization:
        response = jsonify(
            status="fail",
            message="Organization does not exist."
        )
        response.status_code = HTTPStatus.NOT_FOUND
        return response

    # Create a new session bound to the organization's engine
    Session = sessionmaker(bind=organization.get_engine())
    session = Session()
    
    # Use a text object to set the search path
    session.execute(text(f"SET search_path TO {organization.name}"))

    try:
        username = user_data.get("name")
        if User.find_by_name(username):
            response = jsonify(
                status="fail",
                message="User already exists."
            )
            response.status_code = HTTPStatus.CONFLICT
            return response

        new_user = User(**user_data)
        session.add(new_user)  # Add the new_user to the session bound to the organization's schema
        session.commit()  # Commit the session transaction

        response = jsonify(
            status="success",
            message="User created successfully.",
        )
        response.status_code = HTTPStatus.CREATED
        response.headers["Location"] = url_for(
            "api.user", id=new_user.id, _external=True
        )
        response.headers["Cache-Control"] = "no-store"
        response.headers["Pragma"] = "no-cache"
        return response
    except IntegrityError as e:
        session.rollback()
        print(e)
        response = jsonify(
            status="fail",
            error="IntegrityError",
        )
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return response
    except Exception as e:
        session.rollback()
        print(e)
        response = jsonify(
            status="fail",
            error=str(e),
        )
        response.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        return response
    finally:
        session.close()
