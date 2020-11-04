from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy as sa
from application import db, ma


class User(UserMixin, db.Model):

    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'users'

    user_id = sa.Column(sa.String(60), primary_key=True, index=True, unique=True, nullable=False)
    first_name = sa.Column(sa.String(60), nullable=False)
    last_name = sa.Column(sa.String(60), nullable=False)
    username = sa.Column(sa.String(20), index=True, unique=True, nullable=False)
    email = sa.Column(sa.String(60), index=True, unique=True, nullable=False)
    phone = sa.Column(sa.String(20), index=True, unique=True, nullable=False)
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    date_modified = sa.Column(sa.DateTime(timezone=True), onupdate=sa.func.now())
    profile_picture_url = sa.Column(sa.String(200))
    city_id = sa.Column(sa.Integer, default=0)
    town_id = sa.Column(sa.Integer, default=0)
    language = sa.Column(sa.String(20), default='tr')
    device_token = sa.Column(sa.String(200))
    allow_notifications = sa.Column(sa.Boolean, default=True)
    password_hash = sa.Column(sa.String(200))
    is_admin = sa.Column(sa.Boolean, default=False)

    def get_id(self):
        return self.user_id

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class UserSchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        load_only = ['password_hash']
        model = User
        sqla_session = db.session
