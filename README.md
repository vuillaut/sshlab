# sshlab

Jupyter notebook / lab and tensorboard through ssh with a single command and config file

This script is inspired by https://github.com/nicolaschotard/stackyter but reimplemented to allow starting Jupyter in a container (singularity or docker) in the remote server

# Documentation

Visit https://vuillaut.github.io/sshlab/

# Usage

Copy the example settings file `.sshlab_config.yml` to your HOME and edit it to your needs.

## Install


```
pip install sshlab
```

or from source code:

```
pip install .
```

## Run 

```
sshlab -c singularity_config
```

