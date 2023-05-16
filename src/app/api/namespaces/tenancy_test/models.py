from app import db
from sqlalchemy import create_engine
from uuid import uuid4


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, org_id):
        return cls.query.filter_by(id=org_id).first()

    def get_engine(self):
        base_engine = db.get_engine()
        # Update the schema in the connection string
        connection_string = str(base_engine.url)
        connection_string = connection_string.replace("DATABASE", self.name)

        # Create a new engine with the updated connection string
        engine = create_engine(connection_string)

        return engine


class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organization.id"))
    organization = db.relationship("Organization", backref="users")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
