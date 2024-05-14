from sqlalchemy import (Column, Integer, String, ForeignKey, Float, Enum)
from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# creation of the database
engine = create_engine("mysql+mysqlconnector://root:@localhost""/cardeal",
                       echo=None)
Base = declarative_base()


# creation of the tables
class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    email = Column(String(50))
    adverts = relationship("Advert", back_populates="user",
                           cascade="all, delete, delete-orphan")
    proposed_offers = relationship("ProposeOffer", back_populates="user",
                                   cascade="all, delete, delete-orphan")


class Category(Base):
    __tablename__ = 'category'
    id_category = Column(Integer, primary_key=True, autoincrement=True)
    car_category = Column(String(50), nullable=False)
    adverts = relationship("Advert", back_populates="category",
                           cascade="all, delete, delete-orphan")


class Offer(Base):
    __tablename__ = 'offer'
    id_offer = Column(Integer, primary_key=True, autoincrement=True)
    state_offer = Column(Enum('pending', 'accepted', 'refused'), nullable=False)
    price_proposed = Column(Float, nullable=False)

    proposed_offers = relationship("ProposeOffer", back_populates="offer",
                                   cascade="all, delete, delete-orphan")


class Advert(Base):
    __tablename__ = 'advert'
    id_advert = Column(Integer, primary_key=True, autoincrement=True)
    transaction = Column(String(50), nullable=False)
    location = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(400))
    id_category = Column(Integer, ForeignKey('category.id_category'))
    id_user = Column(Integer, ForeignKey('users.id_user'))
    category = relationship("Category", back_populates="adverts")
    user = relationship("User", back_populates="adverts")
    car = relationship("Car", back_populates="advert", uselist=False,
                       cascade="all, delete, delete-orphan")
    proposed_offers = relationship("ProposeOffer", back_populates="advert",
                                   cascade="all, delete, delete-orphan")


class Car(Base):
    __tablename__ = 'car'
    id_car = Column(Integer, primary_key=True, autoincrement=True)
    model_car = Column(String(50), nullable=False)
    car_brand = Column(String(50), nullable=False)
    car_state = Column(Enum('new', 'used'), nullable=False)
    id_advert = Column(Integer, ForeignKey('advert.id_advert'), unique=True)
    advert = relationship("Advert", back_populates="car")


class ProposeOffer(Base):
    __tablename__ = 'propose_offer'
    id_user = Column(Integer, ForeignKey('users.id_user'), primary_key=True)
    id_offer = Column(Integer, ForeignKey('offer.id_offer'), primary_key=True)
    id_advert = Column(Integer, ForeignKey('advert.id_advert'))
    user = relationship("User", back_populates="proposed_offers")
    offer = relationship("Offer", back_populates="proposed_offers")
    advert = relationship("Advert", back_populates="proposed_offers")


# Configuration de la connexion à la base de données (à adapter selon votre cas)
Base.metadata.create_all(engine)

# Création et utilisation d'une session pour interagir avec la base de données
Session = sessionmaker(bind=engine)
session = Session()
session.commit()
session.close()
