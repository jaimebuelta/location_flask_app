import http.client
from datetime import datetime
from flask_restplus import Namespace, Resource, fields
from locations.models import Product, Location
from locations.db import db

api_namespace = Namespace('api', description='API operations')


# Input and output formats for Product
product_parser = api_namespace.parser()
product_parser.add_argument('product_description', type=str,
                            help='Description of the product')

model = {
    'product_id': fields.Integer(attribute='id'),
    'product_description': fields.String(attribute='description'),
}
product_model = api_namespace.model('Product', model)


@api_namespace.route('/product/')
class ProductsListCreate(Resource):

    @api_namespace.doc('list_products')
    @api_namespace.marshal_with(product_model)
    def get(self):
        products = Product.query.order_by('id').all()
        return products

    @api_namespace.doc('create_products')
    @api_namespace.expect(product_parser)
    def post(self):
        args = product_parser.parse_args()

        new_product = Product(description=args['product_description'])
        db.session.add(new_product)
        db.session.commit()

        result = api_namespace.marshal(new_product, product_model)

        return result, http.client.CREATED


@api_namespace.route('/product/<int:product_id>')
class ProductsRetrieveDestroy(Resource):

    @api_namespace.doc('retrieve_product')
    @api_namespace.marshal_with(product_model)
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            # The product is not present
            return None, http.client.NOT_FOUND

        return product

    @api_namespace.doc('delete_product')
    def delete(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            # The product is not present
            return None, http.client.NOT_FOUND

        # Deleting a product required deleting all its locations
        # before
        locations = Location.query.filter_by(product_id=product_id)
        for location in locations:
            db.session.delete(location)

        db.session.delete(product)
        db.session.commit()
        return None, http.client.NO_CONTENT


# Input and output formats for Location
location_parser = api_namespace.parser()
location_parser.add_argument('longitude', required=True, type=float)
location_parser.add_argument('latitude', required=True, type=float)
location_parser.add_argument('elevation', required=True, type=int)

model = {
    'longitude': fields.Float(attribute='longitude'),
    'latitude': fields.Float(attribute='latitude'),
    'elevation': fields.Integer(attribute='elevation'),
    'timestamp': fields.DateTime(attribute='timestamp', dt_format='iso8601'),
}
location_model = api_namespace.model('Location', model)


@api_namespace.route('/product/<int:product_id>/location/')
class LocationListCreate(Resource):

    @api_namespace.doc('list_locations_by_product')
    @api_namespace.marshal_with(location_model)
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return None, http.client.NOT_FOUND

        locations = (Location.query
                     .filter_by(product_id=product_id)
                     .order_by('timestamp')
                     .all())
        return locations

    @api_namespace.doc('create_location_for_product')
    @api_namespace.expect(location_parser)
    def post(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return None, http.client.NOT_FOUND

        args = location_parser.parse_args(strict=True)

        # Generate the timestamp
        timestamp = datetime.utcnow()

        new_location = Location(longitude=args['longitude'],
                                latitude=args['latitude'],
                                elevation=args['elevation'],
                                timestamp=timestamp,
                                product_id=product_id)
        db.session.add(new_location)
        db.session.commit()

        result = api_namespace.marshal(new_location, location_model)

        return result, http.client.CREATED
