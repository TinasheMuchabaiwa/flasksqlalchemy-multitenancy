from datetime import datetime, timedelta

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    kc_user_id = db.Column(db.String(50), unique=True, nullable=False)
    token = db.Column(db.JSON)
    access_token = db.Column(db.String(255))
    token_expiration = db.Column(db.DateTime)

    def __repr__(self):
        return f"<User: {self.username}, {self.email}, {self.admin}>"

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def get_token(self):
        now = datetime.utcnow()
        if self.access_token and self.token_expiration > now + timedelta(seconds=60):
            return self.token

        self.access_token = self.token["access_token"]
        self.token_expiration = now + timedelta(seconds=self.token["expires_in"])
        return self.token

    @staticmethod
    def check_token(access_token):
        user = User.query.filter_by(access_token=access_token).first()
        if not user or user.token_expiration < datetime.utcnow():
            return None
        return user

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=60)

    def valid_token(self):
        if self.token_expiration and self.token_expiration > datetime.utcnow():
            return True
        return False
