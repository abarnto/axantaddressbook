# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in axantaddressbook.

This file complements development/deployment.ini.

"""
from tg import FullStackApplicationConfigurator

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
try:
    # Enable DebugBar if available, install tgext.debugbar to turn it on
    from tgext.debugbar import enable_debugbar
    enable_debugbar(base_config)
except ImportError:
    pass
