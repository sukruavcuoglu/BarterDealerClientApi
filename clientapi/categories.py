"""
This is the people module and supports all the REST actions for the
people data
"""

from clientapi.models.categories import Category, CategorySchema


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of categories

    :return:        json string of list of people
    """
    # Create the list of people from our data
    categories = Category.query.order_by(Category.date_created).all()

    # Serialize the data for the response
    category_schema = CategorySchema(many=True)
    data = category_schema.dump(categories)
    return data
