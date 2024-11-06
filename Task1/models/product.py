import logging
from sqlalchemy.sql import func
from models import db

logger = logging.getLogger()

class DataValidationError(Exception):
    """Used for data validation errors when deserializing"""

class Product(db.Model):
    """ Class that represents a Product """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(64))
    price = db.Column(db.Float, nullable=True)  # Changed to Float
    disabled = db.Column(db.Boolean(), nullable=False, default=False)
    date_purchase = db.Column(db.Date, nullable=False, server_default=func.now())
    stock_quantity = db.Column(db.Integer, nullable=False)  # Removed primary_key=True

    def __repr__(self):
        return '<Product %r>' % self.name

    def to_dict(self) -> dict:
        """Serializes the class as a dictionary"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def from_dict(self, data: dict) -> None:
        """Sets attributes from a dictionary"""
        for key, value in data.items():
            setattr(self, key, value)

    def create(self):
        """Creates a Product in the database"""
        logger.info("Creating %s", self.name)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """Updates a Product in the database"""
        logger.info("Saving %s", self.name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """Removes a Product from the data store"""
        logger.info("Deleting %s", self.name)
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls) -> list:
        """Returns all of the Products in the database"""
        logger.info("Processing all Products")
        return cls.query.all()

    @classmethod
    def find(cls, product_id: int):
        """Finds a Product by its ID"""
        logger.info("Processing lookup for id %s ...", product_id)
        return cls.query.get(product_id)
