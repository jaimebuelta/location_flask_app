import http.client
from flask_restplus import Namespace, Resource, fields
from locations.models import Product
from locations.db import db

api_namespace = Namespace('api', description='API operations')

product_parser = api_namespace.parser()
product_parser.add_argument('product_description')

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
        products = Product.query.all()
        return products

    @api_namespace.doc('create_products')
    @api_namespace.expect(product_parser)
    def post(self):
        args = product_parser.parse_args()

        new_product = Product(description=args['product_description'])
        db.session.add(new_product)
        db.session.commit()

        return api_namespace.marshal(new_product, product_model), http.client.CREATED


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

        db.session.delete(product)
        db.session.commit()
        return None, http.client.NO_CONTENT
