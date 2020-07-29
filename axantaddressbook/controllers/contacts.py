from axantaddressbook.lib.base import BaseController
from tg import expose, redirect
from axantaddressbook.model import DBSession
from axantaddressbook.model.contact import Contact
from phonenumbers import format_number, PhoneNumberFormat


class ContactsController(BaseController):

    @expose('axantaddressbook.templates.contacts-list')
    def index(self):
        contacts = DBSession.query(Contact).all()
        contacts = list(map(self.__getContactWithFormattedPhone, contacts))
        return dict(contacts=contacts)

    
    @expose('axantaddressbook.templates.new-contact')
    def new(self):
        return dict()


    @expose()
    def add(self, **form):
        contact = Contact(name=form.get('name'), surname=form.get('surname'), phone=form.get('phone'))
        DBSession.add(contact)
        DBSession.flush()
        redirect('/')


    def __getContactWithFormattedPhone(self, contact):
        contact.phone = format_number(contact.phone, PhoneNumberFormat.INTERNATIONAL)
        return contact