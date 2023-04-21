.. _building-docs:

Building the Documentation
==========================

This section provides instructions on how to build the documentation locally for development and testing purposes.

Prerequisites
-------------

Install `sshlab` with doc requirements after cloning the repository:

.. code-block:: console

   pip install -e ".[doc]"

Building the Documentation
--------------------------

To build the documentation, navigate to the `docs` directory in the project root and run the following command:

.. code-block:: console

   make clean html

This command generates the HTML documentation in the `build/html` directory within the `docs` folder.

To view the generated documentation, open the `index.html` file located in the `build/html` directory with your web browser.

.. note::

   If you make any changes to the documentation, you need to rebuild it using the `make html` command.
