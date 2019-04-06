from flask_restplus import Namespace, Resource

api_namespace = Namespace('api', description='API operations')


@api_namespace.route('/products')
class ProductsList(Resource):

    @api_namespace.doc('list_products')
    def get(self):
        return []
