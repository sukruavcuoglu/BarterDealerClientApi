import sqlalchemy as sa
from application import db, ma


class Category(db.Model):

    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'categories'

    category_id = sa.Column(sa.String(60), primary_key=True, index=True, unique=True, nullable=False)
    title = sa.Column(sa.String(20), index=True, unique=True, nullable=False)
    date_created = sa.Column(sa.DateTime(timezone=True), server_default=sa.func.now())
    date_modified = sa.Column(sa.DateTime(timezone=True), onupdate=sa.func.now())
    image_url = sa.Column(sa.String(200))
    parent_category_id = sa.Column(sa.Integer, sa.ForeignKey('categories.category_id'))


class CategorySchema(ma.ModelSchema):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    class Meta:
        model = Category
        sqla_session = db.session
