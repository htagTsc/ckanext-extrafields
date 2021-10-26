import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

def create_contributorID_tags():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'contributorID_tags'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'contributorID_tags'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'https://opendata-beispielstadt.de', u'https://opendata-beispielstadtXY.de'):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def contributorID_tags():
    create_contributorID_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        contributorID_tags = tag_list(data_dict={'vocabulary_id': 'contributorID_tags'})
        return contributorID_tags
    except toolkit.ObjectNotFound:
        return None

class ExtrafieldsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def get_helpers(self):
        return {
            'contributorID_tags': contributorID_tags
            }


    def _modify_package_schema(self, schema):
        schema.update({
            'contributorID': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')('contributorID_tags')]
        })
        schema.update({
            'plannedAvailability': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'politicalGeocodingLevelURI': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'politicalGeocodingURI': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'geocodingDescription': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'licenseAttributionByText': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'startDate': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'endDate': [toolkit.get_validator('ignore_missing'),
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
        
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'contributorID': [
                tk.get_converter('convert_from_tags')('contributorID_tags'),
                tk.get_validator('ignore_missing')]
        })
        schema.update({
            'contributorID': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'plannedAvailability': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'startDate': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'endDate': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'politicalGeocodingLevelURI': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'politicalGeocodingURI': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'geocodingDescription': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'licenseAttributionByText': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    # IConfigurer
    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        toolkit.add_template_directory(config, 'templates')