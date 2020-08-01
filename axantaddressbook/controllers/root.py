# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, redirect, tmpl_context

from axantaddressbook.lib.base import BaseController
from axantaddressbook.controllers.error import ErrorController
from axantaddressbook.controllers.contacts import ContactsController
from axantaddressbook.controllers.auth import AuthController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the axantaddressbook application.
    """

    error = ErrorController()

    contacts = ContactsController()

    auth = AuthController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "AxantAddressBook"

    @expose()
    def _default(self):
        redirect('/contacts')
