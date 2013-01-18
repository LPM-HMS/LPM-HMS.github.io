"""
A Cosmos session.  Must be the first import of any cosmos script.
"""
import os,sys
from cosmos.Cosmos.helpers import confirm
from cosmos.config import settings

#######################
# DJANGO
#######################

#configure django settings
from cosmos import django_settings
from django.conf import settings as django_conf_settings, global_settings
django_conf_settings.configure(
    TEMPLATE_CONTEXT_PROCESSORS=global_settings.TEMPLATE_CONTEXT_PROCESSORS + ('Workflow.context_processor.contproc',),
    **django_settings.__dict__)



#######################
# DRMAA
#######################

if settings['DRM'] == 'LSF':
    os.environ['DRMAA_LIBRARY_PATH'] = settings['drmaa_library_path']
    os.environ['DRMAA_LIBRARY_PATH'] = os.path.join(settings['cosmos_library_path'],'lsf_drmaa.conf')

import drmaa
drmaa_enabled = False
try:
    drmaa_session = drmaa.Session()
    drmaa_session.initialize()
    drmaa_enabled = True
except Exception as e:
    print e
    print "ERROR! Could not enable drmaa.  Proceeding without drmaa enabled."