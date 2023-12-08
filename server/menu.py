# menu.py
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from config import db
from menudish import MenuDish

class Menu(db.Model, SerializerMixin):
    __tablename__ = 'menus'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    # relationships
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    restaurant = db.relationship('Restaurant', back_populates='menus')
    menu_dish_associations = db.relationship('MenuDish', back_populates='menu', cascade='all, delete-orphan')
    dishes = association_proxy('menu_dish_associations', 'dish')  # Add association_proxy

    reviews = db.relationship('Review', back_populates='menu', cascade='all, delete-orphan')

    # serialization
    serialize_only = ("id", "name", "restaurant_id", "dishes", "reviews")

    def __repr__(self):
        return f"<Menu {self.id}: {self.name}>"

    # validation
    @validates("name")
    def validate_name(self, _, name):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        elif len(name) < 1:
            raise ValueError("Name must be at least 1 character")
        return name

    # Add more validations as needed
