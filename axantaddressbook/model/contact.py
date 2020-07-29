from sqlalchemy.orm import mapper, relation
from sqlalchemy import Column
from sqlalchemy.types import Integer, String
from sqlalchemy_utils.types.phone_number import PhoneNumberType

from axantaddressbook.model import DeclarativeBase, metadata, DBSession

class Contact(DeclarativeBase):
    __tablename__ = 'contacts'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(PhoneNumberType('IT', 10))
    