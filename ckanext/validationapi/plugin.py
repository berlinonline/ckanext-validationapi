"""
Main module for ckanext-validationapi
"""
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IBlueprint
import ckan.plugins.toolkit as toolkit

from ckanext.validationapi import blueprint

class ValidationapiPlugin(SingletonPlugin):
    """
    Main plugin class for ckanext-validationapi
    """
    implements(IConfigurer)
    implements(IBlueprint)

    # IConfigurer:

    def update_config(self, config_):
        """
        Implementation of
        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IConfigurer.update_config
        """
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'validationapi')

    # IBlueprint

    def get_blueprint(self):
        return blueprint.validationapi

