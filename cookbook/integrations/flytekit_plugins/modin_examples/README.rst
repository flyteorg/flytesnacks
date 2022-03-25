Modin
======

Modin is a pandas-accelerator that helps handle large datasets. 
Pandas works gracefully with small datasets since it is inherently single-threaded, and designed to work on a single CPU core. 

With large datasets, the performance of pandas drops (becomes slow or runs out of memory) due to single core usage. 

This is where Modin can be helpful.

Instead of optimizing pandas workflows for a specific setup, we can speed up pandas workflows by utilizing all the resources (cores) available in the system using the concept of ``parallelism``. `Here <https://modin.readthedocs.io/en/stable/getting_started/why_modin/pandas.html#scalablity-of-implementation>`__ is a visual representation of how the cores are utilized in case of Pandas and Modin.


Installation
------------

.. code:: bash

   pip install flytekitplugins-modin

.. note::

   Modin runs with Ray or Dask as the backend. Usage can be specified during the execution itself.


How is Modin different?
-----------------------

Modin **scales** the Pandas workflows by changing only a **single line of code**.

Modin allows the user to utilize all the CPU cores available in the machine. If the same workflow can be run using 4 processors instead of one, why not use it? This way, the time consumed reduces significantly.
