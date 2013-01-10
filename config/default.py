import os 
#os.environ['DJANGO_SETTINGS_MODULE'] = 'cosmos.Cosmos.django_settings'
#os.environ['COSMOS_HOME_PATH'] = '/home/erik/workspace/cosmos'

#######################
# Cosmos
#######################

home_path = os.environ['COSMOS_HOME_PATH']
default_root_output_dir = '/tmp/cosmos_out' # The directory to output all files to
DRM = 'GE' #LSF, or GE
tmp_dir = '/tmp'
default_queue = None #Default Queue name to use if a workflow's default_queue is set to None.

########################
# Web interface
########################

# on some systems, file i/o slows down a lot when running a lot of jobs making file_size calculations very slow.
show_stage_file_sizes = False 
show_jobAttempt_file_sizes = False
show_task_file_sizes = False

########################
# Database
########################

DATABASE = {
    'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
    'NAME': '/home/erik/workspace/Cosmos/sqlite.db',                      # Or path to database file if using sqlite3.
    'USER': '',                      # Not used with sqlite3.
    'PASSWORD': '',                  # Not used with sqlite3.
    'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
    'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
}



### SGE Specific
parallel_environment_name = 'orte' #the name of the SGE parallel environment name.  Use "qconf -spl" to list available names