"""
Main module for ckanext-validationapi
"""
from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IConfigurer
from ckan.plugins import IRoutes
import ckan.plugins.toolkit as toolkit


class ValidationapiPlugin(SingletonPlugin):
    """
    Main plugin class for ckanext-validationapi
    """
    implements(IConfigurer)
    implements(IRoutes, inherit=True)

    # IConfigurer:

    def update_config(self, config_):
        """
        Implementation of
        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IConfigurer.update_config
        """
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'validationapi')

    # IRoutes:

    def before_map(self, map_):
        """
        Implementation of
        https://docs.ckan.org/en/latest/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IRoutes.before_map
        """
        map_.connect(
            '/api/validation/validate',
            controller='ckanext.validationapi.controller:ValidationController',
            action='validate')

        return map_
