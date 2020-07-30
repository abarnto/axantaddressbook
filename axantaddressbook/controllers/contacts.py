from tg import expose, redirect, render_template

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
        form = ContactForm()
        return dict(form=form)


    @expose()
    def add(self, **data):
        data['phone'].replace(" ", "")
        form = ContactForm(MultiDict(data))
        if form.validate():
            contact = Contact(name=form.name.data, surname=form.surname.data, phone=form.phone.data)
            DBSession.add(contact)
            DBSession.flush()
            redirect('/')
        else:
            return render_template(dict(form=form), 'jinja', 'axantaddressbook.templates.new-contact')


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
    name = StringField('Nome *', [validators.DataRequired()])
    surname = StringField('Cognome')
    phone = StringField('N° Telefono *', [validators.Regexp('^[0-9]+$', message="Sono ammessi solo numeri"), validators.Length(min=9, max=10, message="Il N° di telefono deve avere 9 o 10 cifre"), validators.DataRequired()])


class MultiDict(dict):
    def getlist(self, key):
        return self[key] if type(self[key]) == list else [self[key]]

    def __repr__(self):
        return type(self).__name__ + '(' + dict.__repr__(self) + ')'