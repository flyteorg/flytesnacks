Modin
======

Modin is a Python extension for Pandas that helps handle large datasets. 
Pandas works gracefully with small datasets since it is inherently single-threaded, and designed to work on a single CPU core. If a dataset is too large to fit in memory, it throws a ``MemoryError``. 

With large datasets, the performance of pandas drops (becomes slow or runs out of memory) due to single core usage. Instead of optimizing pandas workflows for a specific setup, we can speed up pandas workflows by utilizing all the resources (cores) available in the system. This way, the user can focus on the end goal.  

This is where Modin comes into picture. It helps **scale** the Pandas workflows by changing only a **single line of code**.

Installation
------------

.. code:: bash

   pip install flytekitplugins-modin

Why Modin?
----------

Modin helps speed up pandas workflows by up to 4x. It significantly speeds up the Pandas operations, with a single line of import.

Modin allows inplace operations but the **data structures are immutable**. The immutability of data structures is one of the prominent features of Modin, that helps in efficient memory management.

How is Modin different?
-----------------------

Modin allows the user to utilize all the CPU cores available in the machine. If the same workflow can be run using 4 processors instead of one, why not use it? This way, the time consumed reduces significantly.

.. note::

   Modin runs with Ray or Dask as backend. Usage can be specified during execution itself.

Installation
------------

.. code:: bash

   pip install modin[ray]

or

.. code:: bash

   pip install modin[dask]




The magic happens when,

.. code:: bash
	
   import pandas as pd


is changed to:

.. code:: bash

   import modin.pandas as pd


The highlight here is ``parallelism``, i.e. using multiple processors (or cores) for Pandas workflows instead of one. `Here <https://modin.readthedocs.io/en/stable/getting_started/why_modin/pandas.html#scalablity-of-implementation>`__ is a visual representation of how the cores are utilized in case of Pandas and Modin.

