 #!/bin/sh
 
 set -e
 
 cd $CKAN_VENV/src/ckanext-extrafields
 #ckan-python setup.py compile_catalog
 ckan-python setup.py -q install
 
