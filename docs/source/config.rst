.. _config:

Configuration
=============

1. Setup Your Shell Environment
_______________________________


Edit :file:`~/.cosmos/config.ini`, and configure it to your liking.  There are only a few variables to set.

SGE specific environment variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You may also need to set (if they're not already) normal :term:`SGE` job submission variables such as:

.. code-block:: bash

	SGE_ROOT=/opt/sge6/lib/linux-x64/libdrmaa.so
	SGE_EXECD_PORT=63232
	SGE_QMASTER_PORT=63231

3. Create SQL Tables and Load Static Files
__________________________________________

Once you've configured Cosmos, setting up the SQL database tables is easy.  :term:`Django` also requires you to run the collectstatic
command, which moves all the necessary image, css, and javascript files to the static/ directory.  Just run these two commands for any directory after you've properly
configured the environment variables described in step #1.

.. code-block:: bash

   $ cosmos adm syncdb
   $ manage collectstatic