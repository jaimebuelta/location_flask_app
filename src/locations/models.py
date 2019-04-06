from locations.app import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100))


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(db.Integer, db.ForeignKey('product.id'),
                           nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    # Defining longitude and latitude as floats may have issues
    # if there are operations due floating point innacuracy
    # but let's not complicate it at the moment
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Integer, nullable=False)


if __name__ == '__main__':
    # When called in its own, it will initialise the schema
    db.create_all()
