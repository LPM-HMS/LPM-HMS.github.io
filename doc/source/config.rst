Configuration
=============

1. Setup Shell Environment
__________________________

These are environment variables that either :term:`DRMAA`, cosmos, or :term:`Django` require.  Often, its nice to put this
at the end of your ``~/.bashrc`` if you'd like them to be loaded everytime you login.  You must modify the
first two lines.

:file:`libdrmaa.so` is very system and :term:`DRMS` dependent.  Try locations such as these:

* :file:`/opt/lsf/7.0/linux2.6-glibc2.3-x86_64/lib/libdrmaa.so`
* :file:`/usr/lib/libdrmaa.so`
* :file:`/opt/sge6/lib/linux-x64/libdrmaa.so`

.. code-block:: bash
	:emphasize-lines: 1,2

	export COSMOS_HOME_PATH=/path/to/Cosmos          # The path to Cosmos
	export DRMAA_LIBRARY_PATH=/usr/lib/libdrmaa.so       # The path to the :term:`DRMAA` library
	export COSMOS_SETTINGS_MODULE=config.default
	export PYTHONPATH=$COSMOS_HOME_PATH:$PYTHONPATH
	export PATH=$COSMOS_HOME_PATH/bin:$PATH
	export DJANGO_SETTINGS_MODULE=Cosmos.settings

``COSMOS_SETTING_MODULE`` is optional.  By default, cosmos will look for its configuration in ``config/default.py``,
but if you set ``COSMOS_SETTING_MODULE=config.development`` it will load ``config/development.py`` instead.


SGE specific environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may also need to set (if they're not already) normal :term:`SGE` job submission variables such as:

.. code-block:: bash

	SGE_ROOT=/opt/sg
	SGE_EXECD_PORT=63232
	SGE_QMASTER_PORT=63231
   

LSF specific environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following bypasses a bug in :term:`LSF` drmaa v1.04.

.. code-block:: bash
   export LSF_DRMAA_CONF=$COSMOS_HOME_PATH/config/lsf_drmaa.conf
   

2. Edit Configuration File
__________________________

Edit :file:`config/default.py`, and configure it to your liking.  There are only a few variables to set.

.. note:: It is recommended to *not* use an SQL Lite database if the database is stored
on a network shared drive.


3. Create SQL Tables and Load Static Files
__________________________________________

Once you've configured Cosmos, setting up the SQL database tables is easy.  Django requires you to run the collectstatic
command, which moves all the necessary image, css, and javascript files to the static/ directory.

.. code-block:: bash

   $ cosmos adm syncdb
   $ manage collectstatic
   
   