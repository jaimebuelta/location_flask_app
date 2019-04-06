import argparse
import csv
from locations.app import create_app
from locations.models import Product, Location
from locations.db import db


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Add data directly from '
                                     'a CSV file')
    parser.add_argument('-f', type=argparse.FileType('r'))
    args = parser.parse_args()

    application = create_app()
    application.app_context().push()

    csv_reader = csv.DictReader(args.f, delimiter='\t')
    for row in csv_reader:
        # Check the Product
        product = Product.query.get(row['id'])
        if not product:
            product = Product(id=row['id'],
                              description=row['description'])
            db.session.add(product)

        location = Location(product_id=row['id'],
                            timestamp=row['datetime'],
                            latitude=row['latitude'],
                            longitude=row['longitude'],
                            elevation=row['elevation'])
        db.session.add(location)

    db.session.commit()

    # We need to update the sequence for the products, as it has become
    # out of date
    db.session.execute(
        '''
        SELECT setval('product_id_seq',
                COALESCE((SELECT MAX(id)+1 FROM product), 1),
                false);
        '''
    )
