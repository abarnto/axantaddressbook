# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in axantaddressbook.

This file complements development/deployment.ini.

"""
from tg import FullStackApplicationConfigurator

from tgext.pluggable import plug
from tgext.pluggable.template_replacements import replace_template

import axantaddressbook
from axantaddressbook import model, lib

base_config = FullStackApplicationConfigurator()

# General configuration
base_config.update_blueprint({
    # True to prevent dispatcher from striping extensions
    # For example /socket.io would be served by "socket_io"
    # method instead of "socket".
    'disable_request_extensions': False,

    # Set None to disable escaping punctuation characters to "_"
    # when dispatching methods.
    # Set to a function to provide custom escaping.
    'dispatch_path_translator': True,

    'package': axantaddressbook,
})

# ToscaWidgets configuration
base_config.update_blueprint({
    'tw2.enabled': True,
})

# Rendering Engines Configuration
rendering_config = {
    'renderers': ['json'],  # Enable json in expose
    'default_renderer': 'jinja',
}
rendering_config['renderers'].append('jinja')
rendering_config['jinja_extensions'] = ['jinja2.ext.with_']
rendering_config['renderers'].append('kajiki')
# Change this in setup.py too for i18n to work.
rendering_config['templating.kajiki.strip_text'] = False
base_config.update_blueprint(rendering_config)

# Configure Sessions, store data as JSON to avoid pickle security issues
base_config.update_blueprint({
    'session.enabled': True,
    'session.data_serializer': 'json',
})

# Configure the base SQLALchemy Setup
base_config.update_blueprint({
    'use_sqlalchemy': True,
    'model': axantaddressbook.model,
    'DBSession': axantaddressbook.model.DBSession,
})

# This tells to TurboGears how to retrieve the data for your user
from tg.configuration.auth import TGAuthMetadata
class ApplicationAuthMetadata(TGAuthMetadata):
    def __init__(self, dbsession, user_class):
        self.dbsession = dbsession
        self.user_class = user_class

    def authenticate(self, environ, identity):
        login = identity['login']
        user = self.dbsession.query(self.user_class).filter_by(
            email_address=login
        ).first()

        if not user:
            login = None
        elif not user.validate_password(identity['password']):
            login = None

        if login is None:
            try:
                from urllib.parse import parse_qs, urlencode
            except ImportError:
                from urlparse import parse_qs
                from urllib import urlencode
            from tg.exceptions import HTTPFound

            params = parse_qs(environ['QUERY_STRING'])
            params.pop('password', None)  # Remove password in case it was there
            if user is None:
                params['failure'] = 'user-not-found'
            else:
                params['login'] = identity['login']
                params['failure'] = 'invalid-password'

            # When authentication fails send user to login page.
            environ['repoze.who.application'] = HTTPFound(
                location=environ['SCRIPT_NAME'] + '?'.join(('/auth/login', urlencode(params, True)))
            )
        return login

    def get_user(self, identity, userid):
        """
        Used to retireve the user given its userid.
        N.B. If the key is a username, authentication is successfull
        but no repoze.who.identity env variable is populated!!!
        """
        return self.dbsession.query(self.user_class).filter_by(
            email_address=userid
        ).first()

    def get_groups(self, identity, userid):
        return [g.group_name for g in identity['user'].groups]

    def get_permissions(self, identity, userid):
        return [p.permission_name for p in identity['user'].permissions]

# Configure the authentication backend
base_config.update_blueprint({
    'auth_backend': 'sqlalchemy',

    # WARN: In production, this has to be changed!!!
    'sa_auth.cookie_secret': "77475ba2-e355-4792-aac8-a9904629c550", # Same as in development.ini? 
    
    'sa_auth.authmetadata': ApplicationAuthMetadata(model.DBSession, model.User),

    # Page where you want users to be redirected to on login:
    'sa_auth.post_login_url': '/auth/post_login',

    # Page where you want users to be redirected to on logout:
    'sa_auth.post_logout_url': '/auth/post_logout',
    
    # In case ApplicationAuthMetadata didn't find the user discard the whole identity.
    # This might happen if logged-in users are deleted.
    'identity.allow_missing_user': False,

    # override this if you would like to provide a different who plugin for
    # managing login and logout of your application
    'sa_auth.form_plugin': None,
})

try:
    # Enable DebugBar if available, install tgext.debugbar to turn it on
    from tgext.debugbar import enable_debugbar
    enable_debugbar(False)
except ImportError:
    pass

# Configuring tgapp-registration
plug(base_config, 'registration')
plug(base_config, 'tgext.mailer')
replace_template(base_config, 'registration.templates.register', 'axantaddressbook.templates.registration')
replace_template(base_config, 'registration.templates.complete', 'axantaddressbook.templates.registration-complete')
