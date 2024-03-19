#!/usr/bin/python3
""" State Module for HBNB project """

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from models.base_model import BaseModel, Base
import models
from models.place import Place


class Amenity(BaseModel, Base):
    """ Amenities present in the airbnb """

    __tablename__ = "amenities"
    name = Column(String(128), nullable=False)
    place_amenities = relationship('place',
                            secondary='place_amenity',
                            backref='amenities',
                            cascade='delete')
