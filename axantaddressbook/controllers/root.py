# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from axantaddressbook.model import DBSession

from axantaddressbook.lib.base import BaseController
from axantaddressbook.controllers.error import ErrorController

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the axantaddressbook application.
    """

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "axantaddressbook"

    @expose('axantaddressbook.templates.index')
    def index(self):
        """Handle the front-page."""
        return dict(page='index')
