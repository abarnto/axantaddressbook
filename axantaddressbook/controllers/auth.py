from axantaddressbook.lib.base import BaseController

from tg import expose, request, lurl
from tg.flash import flash
from tg.i18n import ugettext as _
from tg.exceptions import HTTPFound

class AuthController(BaseController):
    """ Controller managing repoze.who stuff """

    @expose('axantaddressbook.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if (failure is not None) or (failure is None and login_counter > 0):
            flash(_('Credenziali non corrette. Riprova.'), 'error')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Login Successful: redirect to the initially requested page
        Login Rejected: redirect back to the login page, with a failure object.
        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/auth/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Bentornato, %s!') % userid)

        # Do not use tg.redirect with tg.url as it will add the mountpoint
        # of the application twice.
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.
        """
        flash(_('Arrivederci!'))
        return HTTPFound(location=came_from)
