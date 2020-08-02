from axantaddressbook.tests import TestController

class TestContactsController(TestController):

    # N.B. After each Unit Test, in-memory SQLite DB is deleted!

    def test_empty_list(self):
        """The address book is empty"""
        res = self.app.get('/contacts')
        alertMsg = res.pyquery('#contactsContainer').find('.alert').text()
        assert alertMsg == 'Non ci sono contatti nella rubrica.'

    def test_add(self):
        """Contact addition"""
        additionRes = self.__contact_addition()
        assert additionRes.follow(), additionRes # if redirect happens, insertion is succesful

    def test_filled_list(self):
        """The address book has at least 1 contact"""
        res = self.__contact_addition().follow() # redirect needed in order to render contacts' list page
        cards = res.pyquery('#contactsContainer').find('.card')
        assert len(cards) > 0

    def test_delete(self):
        """Contact deletion"""
        self.__contact_addition() # redirect not needed here
        res = self.app.delete('/contacts/delete', dict(id=1)) # just 1 contact in DB
        assert res.json['success'] == True


    def __contact_addition(self):
        """Using contact form, it populates in-memory db with one contact"""
        page = self.app.get('/contacts/new')

        form = page.form # Returns the only form present in the page, if present; else, it raises an exception.
        form['name'] = 'TestName' # Required | Less than 30 characters
        # form['surname] = 'TestSurname' # Optional | Less than 30 characters
        form['phone'] = 1234567890 # Required | Only numbers | 9 or 10 digits long

        return form.submit()
