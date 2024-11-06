
import factory
from datetime import date
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyFloat
from models.product import Product

class ProductFactory(factory.Factory):
    """ Creates fake products """

    class Meta:
        model = Product

    id = factory.Sequence(lambda n: n)
    name = factory.Faker("name")
    price = FuzzyFloat(1.0, 100.0)  # Random float between 1.0 and 100.0
    disabled = FuzzyChoice(choices=[True, False])
    date_purchase = FuzzyDate(date(2020, 1, 1))
    description = factory.Faker('sentence')
    stock_quantity = factory.Faker('random_int', min=0, max=1500)
