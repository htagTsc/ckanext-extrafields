import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

class ExtrafieldsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)

    def _modify_package_schema(self, schema):
        schema['resources'].update({
            'sprache': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'datum_erzeugung': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'datum_revision': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'aktualisierungsintervall': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'referenzsystem': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'geographische_ausdehnung': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema['resources'].update({
            'politicalGeocodingURI': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })

        return schema

    def create_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ExtrafieldsPlugin, self).show_package_schema()
        schema['resources'].update({
                'sprache' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'datum_erzeugung' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'datum_revision' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'aktualisierungsintervall' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'referenzsystem' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'geographische_ausdehnung' : [ tk.get_validator('ignore_missing') ]
            })
        schema['resources'].update({
                'politicalGeocodingURI' : [ tk.get_validator('ignore_missing') ]
            })
        
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return False

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # IConfigurer
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')
