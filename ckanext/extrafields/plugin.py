import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def create_politicalGeocoding_codes():
    user = toolkitk.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'politicalGeocoding_codes'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'politicalGeocoding_codes'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'https://www.dcat-ap.de/def/politicalGeocoding/stateKey/20100401#05', u'Test'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def politicalGeocoding_codes():
    create_politicalGeocoding_codes()
    try:
        tag_list = toolkit.get_action('tag_list')
        politicalGeocoding_codes = tag_list(data_dict={'vocabulary_id': 'politicalGeocoding_codes'})
        return politicalGeocoding_codes
    except toolkit.ObjectNotFound:
        return None

class ExtrafieldsPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)

    def _modify_package_schema(self, schema):
        schema.update({
            'sprache': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'datum_erzeugung': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'datum_revision': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'aktualisierungsintervall': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'referenzsystem': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'geographische_ausdehnung': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')],
            'politicalGeocodingURI': [toolkit.get_validator('ignore_missing'), toolkit.get_converter('convert_to_extras')('conver_to_tags')('politicalGeocoding_codes')],
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
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'sprache': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'datum_erzeugung': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'datum_revision': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'aktualisierungsintervall': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'referenzsystem': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'geographische_ausdehnung': [toolkit.get_converter('convert_from_extras'), toolkit.get_validator('ignore_missing')],
            'politicalGeocodingURI': [toolkit.get_converter('convert_from_extras')('convert_from_tags')('politicalGeocodingURI_codes'), toolkit.get_validator('ignore_missing')],
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
