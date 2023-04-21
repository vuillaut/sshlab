.. _overview:

Overview
========

Welcome to the sshlab library documentation! 
This library provides a simple and convenient way to start Jupyter Notebook or JupyterLab instances on a remote server through an SSH tunnel. 
It also includes utilities for killing remote Jupyter and Tensorboard processes.

Using the sshlab library
------------------------

The library consists of three main scripts: `sshlab.py`, `sshlab_kill.py`, and `sshtensorboard.py`.

The `sshlab.py` script is used to start a Jupyter instance on a remote server, the `sshlab_kill.py` script is used to kill a remote Jupyter or Tensorboard process, 
and the `sshtensorboard.py` script is used to start a TensorBoard instance on a remote server.

Additionally, the `utils.py` module contains utility functions for checking port availability, getting remote process PIDs, and killing remote processes.

Configuration
-------------

The library relies on a configuration file in YAML format to store user configurations. 
By default, it looks for a file named `.sshlab_config.yml` in the user's home directory, but a different file can be specified using the `--file` command-line option.

Here's an example configuration file:

.. code-block:: yaml

   default:
     SSH:
       user: username
       server: example.com
       ip: 127.0.0.1
       port: 8888
     Environment:
       cmd: singularity
       target: /path/to/singularity/image.sif
       options: --bind /exp_dir/:/exp_dir/
     Jupyter:
       flavor: lab
       options: --no-browser --notebook-dir=/exp_dir/


In this example, the configuration file has a single user configuration named "default."
The configuration specifies the SSH user and server, the environment command (Singularity in this case), the path to the Singularity image, and the Jupyter flavor (lab or notebook).


Starting a remote Jupyter instance
----------------------------------

To start a remote Jupyter instance using the sshlab library, run the `sshlab.py` script:

.. code-block:: bash

   sshlab

By default, it will use the configuration named "default" in the `.sshlab_config.yml` file. If you have multiple configurations, you can specify the configuration to use with the `--config` option:

.. code-block:: bash

   sshlab --config myconfig


Starting a remote TensorBoard instance
--------------------------------------

To start a remote TensorBoard instance using the sshlab library, run the `sshlab-tensorboard` command:

.. code-block:: bash

  sshlab-tensorboard EXP_NAMES

Replace `EXP_NAMES` with a comma-separated list of experiment names. By default, it will use the configuration named "default" in the `.sshlab_config.yml` file. 
If you have multiple configurations, you can specify the configuration to use with the `--config` option:

.. code-block:: bash

   sshlab-tensorboard --config myconfig EXP_NAMES

The config used must include a `Tensorboard` section, such as:

.. code-block:: yaml 

  tensorboard:
  SSH:
    user: username
    server: server.com
    port: 6006
    ip: 127.0.0.1

  Environment:
    cmd: singularity exec
    target: /path/to/image.sif
    options: --bind /exp_dir/:/exp_dir/

  Tensorboard:
    cmd: /opt/conda/envs/glearn/bin/tensorboard
    logdir: /exp_dir/logs


The `logdir` option is the path to the directory containing the TensorBoard logs (where are located the directories of `EXP_NAMES`).

The `options` option is used to specify any additional options to pass to the environment command. 
For example, if you are using Singularity, you can use the `--bind` option to bind a local directory to a directory in the container.


Killing a remote process
------------------------

When closing the SSH connection, the remote process (Jupyter or TensorBoard) should be killed automatically.    
If not, one may run the `sshlab_kill.py` script:

.. code-block:: bash

   sshlab_kill

By default, it will use the configuration named "default" in the `.sshlab_config.yml` file and try to kill a remote Jupyter process.

If you have multiple configurations or want to kill a different process such as tensorboard,

you can specify the configuration to use with the `--config` option and the process name with the `--process` option:

.. code-block:: bash

   sshlab_kill --config myconfig --process myprocess

That's it! You now have a basic understanding of how to use the sshlab library to start and manage remote Jupyter instances.
