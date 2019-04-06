import http.client
from flask import request
from datetime import datetime
from sqlalchemy.orm import joinedload
from flask_restplus import Namespace, Resource, fields
from locations.models import Product, Location
from locations.db import db
from locations.pagination import get_next_page, get_previous_page

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
        '''
        Retrieves all the products
        '''
        products = Product.query.order_by('id').all()
        return products

    @api_namespace.doc('create_products')
    @api_namespace.expect(product_parser)
    def post(self):
        '''
        Create a new product
        '''
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
        '''
        Retrieve a product
        '''
        product = Product.query.get(product_id)
        if not product:
            # The product is not present
            return '', http.client.NOT_FOUND

        return product

    @api_namespace.doc('update_product')
    @api_namespace.expect(product_parser)
    def put(self, product_id):
        '''
        Update a product description
        '''
        product = Product.query.get(product_id)
        if not product:
            # The product is not present
            return '', http.client.NOT_FOUND

        args = product_parser.parse_args()
        product.description = args['product_description']

        db.session.add(product)
        db.session.commit()

        result = api_namespace.marshal(product, product_model)
        return result, http.client.OK

    @api_namespace.doc('delete_product')
    def delete(self, product_id):
        '''
        Delete a product. This will delete all its locations.
        '''
        product = Product.query.get(product_id)
        if not product:
            # The product is not present
            return '', http.client.NOT_FOUND

        # Deleting a product required deleting all its locations
        # before
        locations = Location.query.filter_by(product_id=product_id)
        for location in locations:
            db.session.delete(location)

        db.session.delete(product)
        db.session.commit()
        return '', http.client.NO_CONTENT


# Input and output formats for Location
location_parser = api_namespace.parser()


def longitude_type(raw_value):
    value = float(raw_value)
    if not (-180.0 <= value <= 180.0):
        raise ValueError('Not valid longidude')
    return value


def latitude_type(raw_value):
    value = float(raw_value)
    if not (-90.0 <= value <= 90.0):
        raise ValueError('Not valid latitude')
    return value


location_parser.add_argument('longitude', required=True, type=longitude_type,
                             help='Float number between -180 and 180')
location_parser.add_argument('latitude', required=True, type=latitude_type,
                             help='Float number between -90 and 90')
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
    def get(self, product_id):
        '''
        List all locations for a product
        '''
        product = Product.query.get(product_id)
        if not product:
            return '', http.client.NOT_FOUND

        locations = (Location.query
                     .filter_by(product_id=product_id)
                     .order_by('timestamp')
                     .all())

        result = api_namespace.marshal(locations, location_model)
        return result

    @api_namespace.doc('create_location_for_product')
    @api_namespace.expect(location_parser)
    def post(self, product_id):
        '''
        Add a new location for a product
        '''
        product = Product.query.get(product_id)
        if not product:
            return '', http.client.NOT_FOUND

        args = location_parser.parse_args(strict=True)

        # Generate the timestamp at the time of creation
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


# Input and output formats for AllLocation
model = {
    'product_id': fields.Integer(),
    'description': fields.String(attribute='product.description'),
    'longitude': fields.Float(),
    'latitude': fields.Float(),
    'elevation': fields.Integer(),
    'timestamp': fields.DateTime(dt_format='iso8601'),
}
all_location_model = api_namespace.model('AllLocation', model)

# Pagination parser
pagination_parser = api_namespace.parser()


def positive(raw_value):
    value = int(raw_value)
    if value <= 0:
        raise ValueError('Needs to be a positive integer')
    return value


pagination_parser.add_argument('page', default=1, type=positive)
pagination_parser.add_argument('size', default=100, type=positive)


@api_namespace.route('/location/')
class AllLocationList(Resource):

    @api_namespace.doc('list_all_locations')
    @api_namespace.expect(pagination_parser)
    def get(self):
        '''
        Retrieve all the locations in the system, in paginated format.
        This will display its products
        '''
        pagination = pagination_parser.parse_args()
        size = pagination['size']
        offset = (pagination['page'] - 1) * size

        # Join both tables to return the values
        base_query = (Location.query
                      .options(joinedload(Location.product))
                      .order_by('product_id', 'timestamp'))

        total = base_query.count()
        all_locations = base_query.offset(offset).limit(size).all()

        # Calculate next/last
        next_page = get_next_page(request, pagination, total)
        previous_page = get_previous_page(request, pagination)
        result = api_namespace.marshal(all_locations, all_location_model)
        paginated_format = {
            'next': next_page,
            'previous': previous_page,
            'total': total,
            'result': result,
        }
        return paginated_format
