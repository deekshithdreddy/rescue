from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Reports(Base):
    __tablename__ = 'all_reports'

    id = Column(Integer, primary_key=True, autoincrement=True)
    evacuation_site = Column(String(250), nullable=False)
    date = Column(String(250), nullable=False)
    time = Column(String(250), nullable=False)
    situation = Column(String(500), nullable=False)
    affected_pop = Column(String(500), nullable=False)
    displaced = Column(String(500), nullable=False)
    response = Column(String(500), nullable=False)
    preparer = Column(String(250), nullable=False)
    releaser = Column(String(250), nullable=False)
    activate = Column(Boolean, nullable=False)
    inventory = relationship('Inventory', back_populates='reports')

class Inventory(Base):
    __tablename__ = 'inventory'

    class ItemEnum:
        rice = "rice"
        flour = "flour"
        water = "water"
        milk = "milk"
        sugar ="sugar"
        canned_goods = "canned goods"
        cooking_oil = "cooking oil"
        blankets = "blankets"
        clothing = "clothing"
        tents = "tents"
        hygiene = "hygiene kits"

    id = Column(Integer, primary_key=True)
    item = Column(String(250), nullable=False, default=ItemEnum.rice)
    quantity = Column(Integer, nullable=False)
    is_available = Column(Boolean, nullable=False)
    evacuation_site = Column(String(250),
                             ForeignKey('all_reports.evacuation_site'),
                             nullable=False)
    reports = relationship('Reports', back_populates='inventory')


engine = create_engine('sqlite:///reports.db')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)