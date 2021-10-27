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
        for tag in (u'Beispielstadt ID', u'  '):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def create_politicalGeocodingURI_tags():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'politicalGeocodingURI_tags'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'politicalGeocodingURI_tags'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Beispielstadt', u'  '):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def create_plannedAvailability_tags():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'plannedAvailability_tags'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'plannedAvailability_tags'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Verfügbar', u'  '):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def create_politicalGeocodingLevelURI_tags():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'politicalGeocodingLevelURI_tags'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'politicalGeocodingLevelURI_tags'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Kommune', u'  '):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def create_licenseAttributionByText_tags():
    user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
    context = {'user': user['name']}
    try:
        data = {'id': 'licenseAttributionByText_tags'}
        toolkit.get_action('vocabulary_show')(context, data)
    except toolkit.ObjectNotFound:
        data = {'name': 'licenseAttributionByText_tags'}
        vocab = toolkit.get_action('vocabulary_create')(context, data)
        for tag in (u'Die Daten wurden mit freundlicher Unterstützung der Beispielstadt bereitgestellt.', u'  '):
            data = {'name': tag, 'vocabulary_id': vocab['id']}
            toolkit.get_action('tag_create')(context, data)

def plannedAvailability_tags():
    create_plannedAvailability_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        plannedAvailability_tags = tag_list(data_dict={'vocabulary_id': 'plannedAvailability_tags'})
        return plannedAvailability_tags
    except toolkit.ObjectNotFound:
        return None

def contributorID_tags():
    create_contributorID_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        contributorID_tags = tag_list(data_dict={'vocabulary_id': 'contributorID_tags'})
        return contributorID_tags
    except toolkit.ObjectNotFound:
        return None

def politicalGeocodingLevelURI_tags():
    create_politicalGeocodingLevelURI_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        politicalGeocodingLevelURI_tags = tag_list(data_dict={'vocabulary_id': 'politicalGeocodingLevelURI_tags'})
        return politicalGeocodingLevelURI_tags
    except toolkit.ObjectNotFound:
        return None

def politicalGeocodingURI_tags():
    create_politicalGeocodingURI_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        politicalGeocodingURI_tags = tag_list(data_dict={'vocabulary_id': 'politicalGeocodingURI_tags'})
        return politicalGeocodingURI_tags
    except toolkit.ObjectNotFound:
        return None

def licenseAttributionByText_tags():
    create_licenseAttributionByText_tags()
    try:
        tag_list = toolkit.get_action('tag_list')
        licenseAttributionByText_tags = tag_list(data_dict={'vocabulary_id': 'licenseAttributionByText_tags'})
        return licenseAttributionByText_tags
    except toolkit.ObjectNotFound:
        return None

class ExtrafieldsPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)

    def get_helpers(self):
        return {
            'contributorID_tags': contributorID_tags,
            'plannedAvailability_tags' : plannedAvailability_tags,
            'politicalGeocodingLevelURI_tags' : politicalGeocodingLevelURI_tags,
            'politicalGeocodingURI_tags' : politicalGeocodingURI_tags,
            'licenseAttributionByText_tags' : licenseAttributionByText_tags
            }


    def _modify_package_schema(self, schema):
        schema.update({
            'contributorID': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_tags')('contributorID_tags')]
        })
        schema.update({
            'plannedAvailability': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_tags')('plannedAvailability_tags')]
        })
        schema.update({
            'politicalGeocodingLevelURI': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_tags')('politicalGeocodingLevelURI_tags')]
        })
        schema.update({
            'politicalGeocodingURI': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_tags')('politicalGeocodingURI_tags')]
        })
        schema.update({
            'geocodingDescription': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'licenseAttributionByText': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_tags')('licenseAttributionByText_tags')]
        })
        schema.update({
            'startDate': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'endDate': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'geometry': [toolkit.get_validator('ignore_missing'),
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
                toolkit.get_converter('convert_from_tags')('contributorID_tags'),
                toolkit.get_validator('ignore_missing')]
        })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'plannedAvailability': [
                toolkit.get_converter('convert_from_tags')('plannedAvailability_tags'),
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
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'politicalGeocodingLevelURI': [
                toolkit.get_converter('convert_from_tags')('politicalGeocodingLevelURI_tags'),
                toolkit.get_validator('ignore_missing')]
        })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'politicalGeocodingURI': [
                toolkit.get_converter('convert_from_tags')('politicalGeocodingURI_tags'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'geocodingDescription': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema.update({
            'geometry': [toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('ignore_missing')]
            })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'licenseAttributionByText': [
                toolkit.get_converter('convert_from_tags')('licenseAttributionByText_tags'),
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