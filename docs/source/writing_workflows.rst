.. _writing_workflows:

Writing Workflows with EZFlow
=============================

The easiest way to write a workflow is to use the *ezflow* package.

.. seealso::
    There are a lot of useful examples.  Some of the more advanced examples even demonstrate
    useful advanced features that are not described here yet.
    :ref:`examples`

.. py:module:: cosmos.contrib.ezflow

*EZFlow* is a package that contains powerful modules for describing workflows.
It allows you to define classes that represent
a command line tool and various functions to make creating a complex workflow of jobs represented by a
:term:`DAG` simple.

A `DAG` consists of Stages, Tools and Tool dependencies.

Defining Tools
--------------

A tool represents an executable (like echo, cat, or paste, or script) that is run from the command line.
A tool is a class that overrides :py:class:`~tool.Tool`, and defines :py:meth:`~tool.Tool.cmd`,
(unless the tool doesn't actually perform an operation, ie
:py:attr:`tool.Tool.NOOP` == True).

.. code-block:: python

    from cosmos.contrib.ezflow.tool import Tool

    class WordCount(Tool):
        name = "Word Count"
        inputs = ['txt']
        outputs = ['txt']
        mem_req = 1*1024
        cpu_req = 1

        def cmd(self,i,s,p):
            return r"""
                wc {i[txt][0]} > $OUT.txt
                """

This tool will read a txt file, count the number of words, and write it to another text file.


See the :py:class:`Tool API <tool.Tool>` for more properties that can be overridden to obtain
various behaviors.


Defining Input Files
--------------------

An Input file is an instantiation of :py:class:`tool.INPUT`, which is just a Tool with
:py:attr:`tool.INPUT.NOOP` set to True, and a way to initialize it with a single output file from an existing
path on the filesystem.

An INPUT has one outputfile, which is an instance of :py:class:`Workflow.models.TaskFile`.  It has 3 important
attributes:

* ``name``: This is the name of the file, and is used as the key for obtaining it.  No Tool an
    have multiple TaskFiles with the same name.  Defaults to ``fmt``.
* ``fmt``: The format of the file.  Defaults to the extension of ``path``.
* ``path``: The path to the file. Required.

Here's an example of how to create an instance of an :py:class:`tool.INPUT` File:

.. code-block:: python

    from cosmos.contrib.ezflow import INPUT

    input_file = INPUT('/path/to/file.txt',tags={'i':1})

``input_file`` will now be a tool instance with an output file called 'txt' that points to :file:`/path/to/file.txt`.

A more fine grained approach to defining input files:

.. code-block:: python

    from cosmos.contrib.ezflow import INPUT
    INPUT(name='favorite_txt',path='/path/to/favorite_txt.txt.gz',fmt='txt.gz',tags={'color':'red'})

Designing Workflows
--------------------

All jobs and and job dependencies are represented by the :py:class:`dag.DAG` class.

There are 5 infix operators you can use to generate a DAG.  They each take an
instance of a :py:class:`~dag.DAG` on the left, and apply the :py:class:`tool.Tool` class
on the right to the last :py:class:`cosmos.Workflow.models.Stage` added to the ``DAG``.

.. hint::

    You can always visualize the ``DAG`` that you've built using :py:meth:`dag.DAG.create_dag_img`.
    (see :ref:`examples` for details)

*The 5 infix operators are:*

.. automethod:: cosmos.contrib.ezflow.dag.DAG.add_
.. automethod:: cosmos.contrib.ezflow.dag.DAG.map_
.. automethod:: cosmos.contrib.ezflow.dag.DAG.reduce_
.. automethod:: cosmos.contrib.ezflow.dag.DAG.split_
.. automethod:: cosmos.contrib.ezflow.dag.DAG.reduce_split_


    .. code-block:: python

.. py:method:: |Reduce|

    Creates many2one relationships for each tool in the stage last added to the dag grouped by ``keywords``,
    with a new tool of type ``tool_class``.

    :param keywords: (list of str) Tags to reduce to.  All keywords not listed will not be passed on to the tasks generated.
    :param tool_class: (subclass of Tool)
    :param stage_name: (str) The name of the stage.  Defaults to the tool_class.name.
    :returns: The modified dag.

    >>> dag() |Reduce| (['shape','color'],Tool_Class)

    In the above example, the most recent stage will be grouped into tools with the same `shape` and `color`, and a
    dependent tool of type ``tool_class`` will be created tagged with the `shape` and `color` of their parent group.

.. py:method:: |ReduceSplit|

    Creates many2one relationships for each tool in the stage last added to the dag grouped by ``keywords`` and split
    by the product of ``split_by``,
    with a new tool of type ``tool_class``.

    :param keywords: (list of str) Tags to reduce to.  All keywords not listed will not be passed on to the tasks generated.
    :param split_by: (list of (str,list)) Tags to split by.
    :param tool_class: (subclass of Tool)
    :param stage_name: (str) The name of the stage.  Defaults to the tool_class.name.
    :returns: The modified dag.

    >>> dag() |ReduceSplit| (['color','shape'],[('size',['small','large'])],Tool_Class)

    The above example will group the last stage into tools with the same `color` and `shape`, and create
    two new dependent tools with tags ``{'size':'large'}`` and ``{'size':'small'}``, plus the ``color`` and ``shape``
    of their parents.

API
-----------

Tool
*****
.. automodule:: cosmos.contrib.ezflow.tool
    :members:


DAG
****

.. automodule:: cosmos.contrib.ezflow.dag
    :private-members:
    :members:
    :undoc-members:

