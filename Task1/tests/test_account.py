import json
from random import randrange
from unittest import TestCase
from models.product import Product, DataValidationError

from models import db, create_app  # Import create_app to initialize your app

class TestProductModel(TestCase):
    """Test Product Model"""

    @classmethod
    def setUpClass(cls):
        """Load data needed by tests"""
        cls.app = create_app()  # Create the app
        cls.app.app_context().push()  # Push the app context for database operations
        db.create_all()  # Make our SQLAlchemy tables
        global Product_DATA
        with open('tests/fixtures/account_data.json') as json_data:  # Ensure correct filename
            Product_DATA = json.load(json_data)

    @classmethod
    def tearDownClass(cls):
        """Disconnect from the database"""
        db.session.remove()
        db.drop_all()  # Drop all tables at the end of tests

    def setUp(self):
        """Truncate the tables before each test"""
        self.rand = randrange(0, len(Product_DATA))
        db.session.query(Product).delete()
        db.session.commit()

    def tearDown(self):
        """Remove the session after each test"""
        db.session.remove()


    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_all_products(self):
        """ Test creating multiple Products """
        for data in Product_DATA:
            product = Product(**data)
            product.create()
        self.assertEqual(len(Product.all()), len(Product_DATA))

    def test_create_an_product(self):
        """ Test Product creation using known data """
        data = Product_DATA[self.rand]  # get a random Product
        product = Product(**data)
        product.create()
        self.assertEqual(len(Product.all()), 1)

    def test_repr(self):
        """Test the representation of a product"""
        product = Product()
        product.name = "Foo"
        self.assertEqual(str(product), "<Product 'Foo'>")

    def test_to_dict(self):
        """ Test Product to dict """
        data = Product_DATA[self.rand]  # get a random Product
        product = Product(**data)
        result = product.to_dict()
        self.assertEqual(product.name, result["name"])
        self.assertEqual(product.description, result["description"])
        self.assertEqual(product.price, result["price"])
        self.assertEqual(product.disabled, result["disabled"])
        self.assertEqual(product.date_purchase, result["date_purchase"])
        self.assertEqual(product.stock_quantity, result["stock_quantity"])

    def test_from_dict(self):
        """ Test Product from dict """
        data = Product_DATA[self.rand]  # get a random Product
        product = Product()
        product.from_dict(data)
        self.assertEqual(product.name, data["name"])
        self.assertEqual(product.description, data["description"])
        self.assertEqual(product.price, data["price"])
        self.assertEqual(product.disabled, data["disabled"])
        self.assertEqual(product.date_purchase, data["date_purchase"])
        self.assertEqual(product.stock_quantity, data["stock_quantity"])

    def test_update_an_product(self):
        """ Test Product update using known data """
        data = Product_DATA[self.rand]  # get a random product
        product = Product(**data)
        product.create()
        self.assertIsNotNone(product.id)
        product.name = "Updated Product Name"
        product.update
