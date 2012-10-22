Getting Started
===============

We'll start by running a simple test workflow, exploring it via the web interface, and terminating.  Then
you'll be ready to start your own.

Command Line Interface
______________________

Make sure your environment variables, are set.  In particular :file:`/path/to/Cosmos/bin` must be in your PATH
Use the shell command :command:`env` if you're not sure what's in your environment.

.. code-block:: bash

   $ cosmos -h
   usage: cli.py [-h] {adm,wf} ...
   
   positional arguments:
     {adm,wf}
       adm       Admin
       wf        Workflow
   
   optional arguments:
     -h, --help  show this help message and exit
         
Explore the available commands, using -h if you wish.  Or see the :doc:`cli` for more info.  Note that when
listing workflows, the number beside each Workflow inside brackets, `[#]`, is the ID of that object.


Execute the Test Workflow
_________________________
   
The console will generate a lot of output as the workflow runs.  This workflow tests out various
features of Cosmos.  Again, the number beside each object inside brackets, `[#]`, is the ID of that object.

.. code-block:: generic

   $ python /path/to/cosmos/my_workflows/testflow.py
   
   INFO: 2012-09-27 16:47:08: Deleting directory /nas/erik/cosmos_out/Test_Workflow
   INFO: 2012-09-27 16:47:30: Created Workflow Workflow[3] Test Workflow.
   INFO: 2012-09-27 16:47:31: Restarting this Workflow.
   INFO: 2012-09-27 16:47:31: Adding batch Job_That_Runs_Too_Long.
   INFO: 2012-09-27 16:47:31: Creating Batch[352] Job That Runs Too Long from scratch.
   INFO: 2012-09-27 16:47:31: Created node Node[7145] 1 from scratch
   INFO: 2012-09-27 16:47:31: Running batch Batch[352] Job That Runs Too Long.
   INFO: 2012-09-27 16:47:31: Running Node[7145] 1 from Batch[352] Job That Runs Too Long
   INFO: 2012-09-27 16:47:32: Submitted jobAttempt with drmaa jobid 14173
   INFO: 2012-09-27 16:47:32: Adding batch Echo.
   INFO: 2012-09-27 16:47:35: Creating Batch[353] Echo from scratch.
   INFO: 2012-09-27 16:47:35: Created node Node[7146] 1 from scratch
   INFO: 2012-09-27 16:47:35: Created node Node[7147] 2 from scratch
   INFO: 2012-09-27 16:47:35: Created node Node[7148] 3 from scratch
   INFO: 2012-09-27 16:47:35: Running batch Batch[353] Echo.
   INFO: 2012-09-27 16:47:35: Running Node[7146] 1 from Batch[353] Echo
   INFO: 2012-09-27 16:47:36: Submitted jobAttempt with drmaa jobid 14174
   INFO: 2012-09-27 16:47:36: Running Node[7147] 2 from Batch[353] Echo
   INFO: 2012-09-27 16:47:40: Submitted jobAttempt with drmaa jobid 14175
   INFO: 2012-09-27 16:47:40: Running Node[7148] 3 from Batch[353] Echo
   INFO: 2012-09-27 16:47:41: Submitted jobAttempt with drmaa jobid 14176
   INFO: 2012-09-27 16:47:41: Waiting on batch Batch[353] Echo...


Launch the Web Interface
________________________

You can use the web interface to explore the history and debug all workflows.  To start it, run:

.. code-block:: bash

   cosmos adm runweb -p 8080
  

.. note:: Currently the system you're running the web interface on must be the same (or have :term:`DRMAA` access to) as the system you're running the workflow on.
   
Visit http://your-ip:8080 to access it.  If you can't access the website, its likely firewalled off; fortunately, the Cosmos website
works well with lynx.  Use the command: :command:`$ lynx 0.0.0.0:8080` 

.. figure:: imgs/webinterface.png
   :width: 75%
   :align: center

Terminating a Workflow
______________________

To terminate a workflow, simply press ctrl+c (or send the process a SIGINT signal).  Cosmos will terminate running jobs and mark them as failed.  You can resume from the point
in the workflow you left off later.

