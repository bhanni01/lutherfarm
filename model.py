#!/usr/bin/env python3
"""Data model"""

from config import db, mm
from flask_wtf import FlaskForm
from marshmallow import fields
from sqlalchemy.orm import backref, relationship
from wtforms import IntegerField, StringField,DecimalField, BooleanField
from wtforms.validators import DataRequired


class Product(db.Model):
    """Product model"""

    id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    name = db.Column(db.String, nullable=False)  
    image_url = db.Column(db.String, nullable=False)  
    description = db.Column(db.Text, nullable=False)  
    availability = db.Column(db.Boolean, default=True)  
    price = db.Column(db.Float, nullable=False)  
    
    def __repr__(self):
        return f"<Product(name={self.name!r}, price={self.price}, available={self.availability})>"




class ProductSchema(mm.SQLAlchemyAutoSchema):
    """Animal schema"""

    class Meta:
        model = Product
      
        load_instance = True

    location = fields.Nested("LocationSchema")





class ProductAddForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    image_url = StringField("Image URL", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    availability = BooleanField("Available")
    price = DecimalField("Price", validators=[DataRequired()])