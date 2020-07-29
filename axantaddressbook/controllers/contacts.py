from tg import expose, redirect

from wtforms import Form, StringField, IntegerField, validators

from axantaddressbook.lib.base import BaseController
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
        form = ContactForm(name="Antonio", surname="Barile")
        return dict(form=form)


    @expose()
    def add(self, **form):
        contact = Contact(name=form.get('name'), surname=form.get('surname'), phone=form.get('phone'))
        DBSession.add(contact)
        DBSession.flush()
        redirect('/')


    @expose('json')
    def delete(self, **kw):
        contactId = kw['id']
        DBSession.query(Contact).filter_by(id=contactId).delete()
        DBSession.flush()
        return dict(success=True)

    def __getContactWithFormattedPhone(self, contact):
        contact.phone = format_number(contact.phone, PhoneNumberFormat.INTERNATIONAL)
        return contact

class ContactForm(Form):
    name = StringField('Nome *', [validators.Required()])
    surname = StringField('Cognome')
    phone = IntegerField('N° Telefono *', [validators.Required(), validators.Length(min=9, max=10)])
